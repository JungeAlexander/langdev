TODO

Installation on PI:

```
# tested under python 3.7 so far
python3 -m virtualenv .venv
source .venv/bin/activate

pip install -f requirements.txt

wget https://www.piwheels.org/simple/numpy/numpy-1.18.5-cp37-cp37m-linux_armv7l.whl#sha256=4eef6b751109451a94d77828f4bb264929b573a2bb7de8230f59c55722e3caae
pip install numpy-1.18.5-cp37-cp37m-linux_armv7l.whl

wget https://www.piwheels.org/simple/scipy/scipy-1.4.1-cp37-cp37m-linux_armv7l.whl#sha256=ef4e1b837ece171cb99a957a68d2320e7e3c649e0008ed4efb62851f2ff45bf0
pip install scipy-1.4.1-cp37-cp37m-linux_armv7l.whl

rm numpy-1.18.5-cp37-cp37m-linux_armv7l.whl scipy-1.4.1-cp37-cp37m-linux_armv7l.whl
```

Crontab:

```
*/5 * * * * /bin/bash /home/ajunge/code/langdev/filter_chunks.sh 1>/dev/null 2>>/home/ajunge/code/langdev/filter_chunks.log
```

Running recording (best in tmux):

```
source .venv/bin/activate

python record_chunks.py
```