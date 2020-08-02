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
from scipy.io.wavfile import read as read_wavfile

data_dir = "data"
s3_client = boto3.client("s3")

start_time = datetime.now()
output_dir = os.path.join(data_dir, start_time.strftime("%Y%m%d"))
glob_pattern = os.path.join(output_dir, "*.wav")
filter_on_max_signal = False
expected_len = 60 * 5


def get_max_absolute_signal_len(wav_file):
    samplerate, data = read_wavfile(wav_file)
    return np.abs(data).max(), data.shape[0] / samplerate


for wav_file in glob(glob_pattern):
    # print(wav_file)
    max_signal, wav_len = get_max_absolute_signal_len(wav_file)
    wav_len_as_expected = math.isclose(expected_len, wav_len, rel_tol=0.01)
    if not wav_len_as_expected:
        logging.warning(f"wav length not as expected: {wav_len}")
    # print(max_signal)
    if filter_on_max_signal and max_signal < 20000:
        os.remove(wav_file)
    else:
        mp3_file = wav_file[: -len(".wav")] + ".mp3"
        subprocess.run(
            f"lame --preset standard {wav_file} {mp3_file}", shell=True, check=True
        )
        mp3_len = AudioSegment.from_mp3(mp3_file).duration_seconds  # in ms
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
                mp3_file, "rbpitv-kbase-ajs-aws", "langdev/" + mp3_file
            )
        except ClientError as e:
            pass
        else:
            if wav_mp3_len_similar and mp3_len_as_expected:
                os.remove(mp3_file)
