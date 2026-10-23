import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer


def get_speech_client():
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    return SpeechSynthesizer(speech_config=speech_config)
