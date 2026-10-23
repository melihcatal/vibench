import azure.cognitiveservices.speech as speechsdk
import os

def get_speech_config():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    return speech_config

def get_speech_recognizer(speech_config, audio_config=None):
    if audio_config is None:
        audio_config = speechsdk.AudioConfig(use_ microphone=True)
    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
