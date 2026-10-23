import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_config = SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

def save_audio(audio_data, file_path):
    with open(file_path, 'wb') as f:
        f.write(audio_data)