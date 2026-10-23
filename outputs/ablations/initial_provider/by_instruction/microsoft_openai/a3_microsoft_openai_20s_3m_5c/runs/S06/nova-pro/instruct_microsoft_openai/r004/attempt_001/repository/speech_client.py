import os
from azure.cognitiveservices.speech import SpeechConfig

def get_speech_config():
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    service_region = os.getenv('AZURE_SPEECH_REGION')
    return SpeechConfig(subscription=speech_key, region=service_region)