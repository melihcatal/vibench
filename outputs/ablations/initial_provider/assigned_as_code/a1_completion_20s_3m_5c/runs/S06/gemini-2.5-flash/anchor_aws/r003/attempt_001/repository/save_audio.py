import os

def save_audio(audio_bytes: bytes, file_path: str):
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
