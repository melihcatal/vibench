import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer


def get_speech_client():
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    return SpeechRecognizer(speech_config=speech_config)
