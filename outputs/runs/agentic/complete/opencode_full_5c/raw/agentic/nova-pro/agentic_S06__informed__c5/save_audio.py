import os
from elevenlabs import Client, Voice, Audio


def save_audio(audio: Audio, file_path: str):
    with open(file_path, "wb") as f:
        f.write(audio.audio)
