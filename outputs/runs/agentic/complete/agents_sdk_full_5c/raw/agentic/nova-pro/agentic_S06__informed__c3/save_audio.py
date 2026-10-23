import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def save_audio(audio_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(audio_data)