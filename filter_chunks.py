from datetime import datetime
from glob import glob
import logging
import math
import subprocess
import os

from botocore.exceptions import ClientError
import boto3
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.io.wavfile import read as read_wavfile

logging.basicConfig(level=logging.INFO)

data_dir = "data"
s3_client = boto3.client("s3")
bucket_name = "rbpitv-kbase-ajs-aws"
mp3_prefix = "langdev/"

start_time = datetime.now()
output_dir = os.path.join(data_dir, start_time.strftime("%Y%m%d"))
glob_pattern = os.path.join(output_dir, "*.wav")
filter_on_max_signal = False
expected_len = 60 * 5


def get_max_absolute_signal_len(wav_file):
    samplerate, data = read_wavfile(wav_file)
    return np.abs(data).max(), data.shape[0] / samplerate

def find_upload_nonsilent_chunks(mp3_segment, bucket_name, bucket_path_prefix):
    chunks = split_on_silence(mp3_segment, min_silence_len=2000, silence_thresh=-40)
    if len(chunks) == 0:
        logging.info("Only found silence.")
        return
    logging.info(f"Found {len(chunks)} non-silent chunks.")
    for i, chunk in enumerate(chunks):
        chunk_file = f"chunk_{i}.mp3"
        chunk_path = bucket_path_prefix + "_" + chunk_file
        chunk.export(
            chunk_file,
            format = "mp3"
        )
        try:
            s3_client.upload_file(
                chunk_file, bucket_name, chunk_path
            )
        except ClientError as e:
            pass
        os.remove(chunk_file)


# TODO extend to day before to fetch recodings made around midnight
for wav_file in glob(glob_pattern):
    # wav_file = data/20200801/20200801-12-07-50.wav
    logging.info(f"Processing {wav_file}.")

    max_signal, wav_len = get_max_absolute_signal_len(wav_file)
    wav_len_as_expected = math.isclose(expected_len, wav_len, rel_tol=0.01)
    if not wav_len_as_expected:
        logging.warning(f"wav length not as expected: {wav_len}")
    # print(max_signal)
    if filter_on_max_signal and max_signal < 20000:
        os.remove(wav_file)
    else:
        mp3_file = wav_file[: -len(".wav")] + ".mp3"
        # mp3_file = data/20200801/20200801-12-07-50.mp3
        chunk_prefix = mp3_prefix + "data/processed/non_silent_splits/" + mp3_file.split("/")[1] + "/" + mp3_file.split("/")[2][: -len(".mp3")]
        subprocess.run(
            f"lame --preset standard {wav_file} {mp3_file} 1>/dev/null 2>/dev/null", shell=True, check=True
        )
        mp3_segment = AudioSegment.from_mp3(mp3_file)
        mp3_len = mp3_segment.duration_seconds  # in ms
        mp3_len_as_expected = math.isclose(expected_len, mp3_len, rel_tol=0.01)
        if not mp3_len_as_expected:
            logging.warning(f"mp3 length not as expected: {mp3_len}")
        wav_mp3_len_similar = math.isclose(mp3_len, wav_len, rel_tol=0.01)
        if not wav_mp3_len_similar:
            logging.warning(f"wav and mp3 length do not match. {wav_len} vs {mp3_len}")
        if wav_mp3_len_similar and wav_len_as_expected:
            os.remove(wav_file)
        try:
            s3_client.upload_file(
                mp3_file, bucket_name, mp3_prefix + mp3_file
            )
        except ClientError as e:
            pass
        else:
            find_upload_nonsilent_chunks(mp3_segment, bucket_name, chunk_prefix)
            if wav_mp3_len_similar and mp3_len_as_expected:
                os.remove(mp3_file)
