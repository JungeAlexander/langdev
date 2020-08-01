import datetime
import os
import subprocess
import sys
import time

data_dir = "data"

def start_recording(start_time, end_time, now_time):
    if start_time < end_time:
        return start_time <= now_time <= end_time
    else: # past midnight
        return now_time >= start_time or now_time <= end_time

while True:
    start_time = datetime.datetime.now()
    recording_start_time = datetime.time(20, 00)
    recording_end_time = datetime.time(6,00)
    output_dir = os.path.join(data_dir, start_time.strftime("%Y%m%d"))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(
        output_dir, start_time.strftime("%Y%m%d-%H-%M-%S") + ".wav"
    )
    recording_duration = 60 * 5

    if not start_recording(recording_start_time, recording_end_time, start_time.time()):
        print(f"{start_time.time()} is not a time to record.")
        time.sleep(60 * 10)
        continue

    for attempt in range(3):
        print(f"Started recording to {output_file} (attempt {attempt}).")
        try:
            subprocess.run(
                f"arecord -D plughw:2 -d {recording_duration} -f cd {output_file}",
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            time.sleep(60)
        else:
            print(f"Finished recording to {output_file}.")
            break
    else:
        print(f"Recording to {output_file} failed. Exiting.")
        sys.exit(1)
