from datetime import datetime
from glob import glob
import subprocess
import os

import numpy as np
from scipy.io.wavfile import read as read_wavfile

data_dir = "data"

start_time = datetime.now()
output_dir = os.path.join(data_dir, start_time.strftime("%Y%m%d"))
glob_pattern = os.path.join(output_dir, "*.wav")

def get_max_absolute_signal(wav_file):
    samplerate, data = read_wavfile(wav_file)
    return np.abs(data).max()

for wav_file in glob(glob_pattern):
    # print(wav_file)
    max_signal = get_max_absolute_signal(wav_file)
    # print(max_signal)
    if max_signal < 20000:
        os.remove(wav_file)
    else:
        mp3_file = wav_file[:-len(".wav")] + ".mp3"
        subprocess.run(f"lame --preset standard {wav_file} {mp3_file}", shell=True, check=True)
        os.remove(wav_file)
        # TODO send mp3 to S3
        # TODO if s3 transfer good, delete mp3
