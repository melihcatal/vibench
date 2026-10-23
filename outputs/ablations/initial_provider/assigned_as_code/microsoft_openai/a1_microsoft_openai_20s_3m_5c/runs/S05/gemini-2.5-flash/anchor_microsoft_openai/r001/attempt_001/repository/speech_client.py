import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    return speech_config

def get_speech_recognizer(speech_config, audio_config=None, language_code="en-US"):
    speech_config.speech_recognition_language = language_code
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    return recognizer
