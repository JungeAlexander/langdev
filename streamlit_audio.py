from glob import glob
import os

import streamlit as st

st.title("Streamlit audio test")

glob_pattern = "data/20200607/*.mp3"
audio_paths = sorted(glob(glob_pattern))
audio_path = st.selectbox("Audio file", audio_paths, 0)

audio_file = open(audio_path, "rb")
audio_bytes = audio_file.read()

st.audio(audio_bytes, format="audio/mp3")
