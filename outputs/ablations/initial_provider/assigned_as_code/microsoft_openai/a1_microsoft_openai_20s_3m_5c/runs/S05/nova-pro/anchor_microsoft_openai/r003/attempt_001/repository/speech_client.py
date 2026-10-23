import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config():
    api_key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION')
    return speechsdk.SpeechConfig(subscription=api_key, region=region)