import boto3

from speech_client import get_speech_client


def save_audio(audio_bytes, file_path):
    with open(file_path, "wb") as f:
        f.write(audio_bytes)