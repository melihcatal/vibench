import os
from azure.cognitiveservices.speech import SpeechConfig

def get_speech_config():
    return SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))