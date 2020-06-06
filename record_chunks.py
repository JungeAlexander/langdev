from datetime import datetime
import os
import subprocess

data_dir = "data"

while True:
    start_time = datetime.now()
    output_dir = os.path.join(data_dir, start_time.strftime("%Y%m%d"))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(
        output_dir, start_time.strftime("%Y%m%d-%H-%M-%S") + ".wav"
    )
    print(f"Started writing to {output_file}.")
    subprocess.run(f"arecord -D plughw:2 -d 60 -f cd {output_file}", shell=True)
    print(f"Finished writing to {output_file}.")
