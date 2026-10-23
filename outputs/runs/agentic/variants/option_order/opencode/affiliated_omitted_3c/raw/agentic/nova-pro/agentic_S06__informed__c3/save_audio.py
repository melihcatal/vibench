import os
from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    AudioDataStream,
)


def save_audio(audio_data, file_path):
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_data)
