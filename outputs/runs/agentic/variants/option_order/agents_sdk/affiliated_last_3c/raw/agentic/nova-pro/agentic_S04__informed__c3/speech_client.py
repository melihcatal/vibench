import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

speech_config = SpeechConfig(subscription=speech_key, region=speech_region)

def get_speech_recognizer():
    return SpeechRecognizer(speech_config=speech_config)