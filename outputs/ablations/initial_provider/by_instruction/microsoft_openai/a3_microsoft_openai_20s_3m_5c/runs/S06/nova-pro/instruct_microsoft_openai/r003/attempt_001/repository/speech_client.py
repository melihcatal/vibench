import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def get_speech_client():
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    return SpeechSynthesizer(speech_config=speech_config)