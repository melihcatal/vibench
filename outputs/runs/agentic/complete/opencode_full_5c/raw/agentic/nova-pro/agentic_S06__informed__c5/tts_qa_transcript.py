import os
from azure.ai.speech import SpeechConfig, SpeechRecognizer


def transcribe_audio(file_path: str) -> str:
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = SpeechConfig(subscription=key, region=region)
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=file_path)
    result = recognizer.recognize_once()
    return result.text
