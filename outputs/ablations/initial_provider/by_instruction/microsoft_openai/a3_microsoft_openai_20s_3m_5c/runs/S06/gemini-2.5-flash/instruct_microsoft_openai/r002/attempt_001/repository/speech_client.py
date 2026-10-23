import azure.cognitiveservices.speech as speechsdk
import os

def get_speech_synthesizer():
    speech_key = os.environ.get('SPEECH_KEY')
    service_region = os.environ.get('SPEECH_REGION')

    if not speech_key or not service_region:
        raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_ Alber_output=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    return speech_synthesizer

def get_speech_recognizer():
    speech_key = os.environ.get('SPEECH_KEY')
    service_region = os.environ.get('SPEECH_REGION')

    if not speech_key or not service_region:
        raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    return speech_recognizer
