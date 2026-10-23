import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config():
    subscription_key = os.getenv('SPEECH_KEY')
    region = os.getenv('SPEECH_REGION')
    return speechsdk.SpeechConfig(subscription=subscription_key, region=region)

def get_audio_config(use_default_microphone=True):
    if use_default_microphone:
        return speechsdk.audio.AudioConfig(use_default_microphone=True)
    else:
        return speechsdk.audio.AudioConfig(filename=os.getenv('AUDIO_FILE'))