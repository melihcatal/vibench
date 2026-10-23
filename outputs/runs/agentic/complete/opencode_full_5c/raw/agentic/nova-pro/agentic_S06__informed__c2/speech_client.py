import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer


def get_speech_credentials():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    return speech_key, service_region


def create_speech_synthesizer():
    speech_key, service_region = get_speech_credentials()
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    return SpeechSynthesizer(speech_config=speech_config)
