from google.cloud import texttospeech
import os


def save_audio(audio_content: bytes, file_path: str = "synthesized_speech.mp3") -> str:
    with open(file_path, "wb") as out_file:
        out_file.write(audio_content)
    return file_path
