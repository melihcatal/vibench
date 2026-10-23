from google.cloud import texttospeech
import os

def save_audio_to_file(audio_content: bytes, filename: str):
    with open(filename, 'wb') as f:
        f.write(audio_content)
