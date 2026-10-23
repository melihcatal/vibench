import azure.cognitiveservices.speech as speechsdk
import os

def get_speech_config(language: str = "en-US"):    
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = language
    return speech_config

def get_audio_config_from_microphone():
    return speechsdk.AudioConfig(use_default_microphone=True)

def get_push_audio_input_stream_config():
    return speechsdk.AudioConfig(stream=speechsdk.audio.PushAudioInputStream())
