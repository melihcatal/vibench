import os
import azure.cognitiveservices.speech as speechsdk


def get_speech_config(api_key, region, language_code):
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language = language_code
    return speech_config


def get_audio_config(stream):
    return speechsdk.audio.AudioConfig(stream=stream)


def get_recognizer(speech_config, audio_config):
    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)