import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config(api_key, region):
    return speechsdk.SpeechConfig(subscription=api_key, region=region)

def get_audio_config(stream):
    return speechsdk.audio.AudioConfig(stream=stream)