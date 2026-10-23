import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
synthesizer = SpeechSynthesizer(speech_config=speech_config)

def save_audio(audio_data, file_path):
    with open(file_path, 'wb') as audio_file:
        audio_file.write(audio_data)