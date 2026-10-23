import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def create_speech_client():
    speech_config = SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))
    return SpeechSynthesizer(speech_config=speech_config)