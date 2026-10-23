import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config():
    subscription_key = os.getenv('SPEECH_SUBSCRIPTION_KEY')
    region = os.getenv('SPEECH_SERVICE_REGION')
    return speechsdk.SpeechConfig(subscription=subscription_key, region=region)

def get_audio_config(use_default_microphone=True):
    return speechsdk.audio.AudioConfig(use_default_microphone=use_default_microphone)