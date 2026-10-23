import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioDataStream

def save_audio(audio_stream: AudioDataStream, file_path: str):
    with open(file_path, 'wb') as file:
        file.write(audio_stream.to_bytes())