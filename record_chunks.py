from datetime import datetime
import os
import subprocess
import sys
import time

data_dir = "data"

while True:
    start_time = datetime.now()
    output_dir = os.path.join(data_dir, start_time.strftime("%Y%m%d"))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(
        output_dir, start_time.strftime("%Y%m%d-%H-%M-%S") + ".wav"
    )
    
    for attempt in range(3):
        print(f"Started recording to {output_file} (attempt {attempt}).")
        try:
            subprocess.run(f"arecord -D plughw:2 -d 60 -f cd {output_file}", shell=True, check=True)
        except subprocess.CalledProcessError:
            time.sleep(60)
        else:
            print(f"Finished recording to {output_file}.")
            break
    else:
         print(f"Recording to {output_file} failed. Exiting.")
         sys.exit(1)
