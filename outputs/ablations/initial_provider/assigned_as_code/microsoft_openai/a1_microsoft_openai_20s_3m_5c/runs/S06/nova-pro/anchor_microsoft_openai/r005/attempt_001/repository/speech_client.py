import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config(config):
    return speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])