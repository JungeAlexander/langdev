from datetime import datetime
from glob import glob
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
    print(wav_file)
    print(get_max_absolute_signal(wav_file))
