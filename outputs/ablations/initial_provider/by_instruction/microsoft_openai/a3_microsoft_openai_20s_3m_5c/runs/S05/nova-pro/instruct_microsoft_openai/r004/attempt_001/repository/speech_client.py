import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig

def get_speech_config():
    subscription_key = os.getenv('SPEECH_KEY')
    region = os.getenv('SPEECH_REGION')
    return SpeechConfig(subscription=subscription_key, region=region)

def get_audio_config(use_default_microphone=True):
    return AudioConfig(use_default_microphone=use_default_microphone)