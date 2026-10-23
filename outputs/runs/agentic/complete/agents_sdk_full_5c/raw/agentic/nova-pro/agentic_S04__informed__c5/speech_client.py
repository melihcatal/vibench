import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

def get_speech_config():
    return SpeechConfig(subscription=speech_key, region=speech_region)

def get_audio_config(audio_file_path):
    return AudioConfig(filename=audio_file_path)