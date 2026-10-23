import azure.cognitiveservices.speech as speechsdk
import os

def get_speech_config():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    return speech_config

def get_audio_config_from_microphone():
    return speechsdk.audio.AudioConfig(use_default_microphone=True)

def get_audio_config_from_push_stream(push_audio_stream):
    return speechsdk.audio.AudioConfig(stream=push_audio_stream)

def get_speech_recognizer(language: str = "en-US"):
    speech_config = get_speech_config()
    speech_config.speech_recognition_language = language
    audio_config = get_audio_config_from_microphone()
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    return speech_recognizer
