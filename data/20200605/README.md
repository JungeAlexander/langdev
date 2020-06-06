```
# See cat /proc/asound/cards
arecord -D plughw:2 -d 60 -f cd test_60.wav
arecord -D plughw:2 -d 60 -f cd almost_silence_60.wav
arecord -D plughw:2 -d 60 -f cd speech_60.wav
# scp "rbpitv:/home/ajunge/code/langdev/data/20200605/*.wav" .
```
