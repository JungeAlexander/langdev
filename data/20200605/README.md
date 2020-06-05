```
# See cat /proc/asound/cards
arecord -D plughw:2 -d 60 -f cd test_60.wav
```