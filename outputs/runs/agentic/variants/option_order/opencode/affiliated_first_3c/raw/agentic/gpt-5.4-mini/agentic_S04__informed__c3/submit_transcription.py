import os

import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config
from speech_models import TranscriptionRequest


def submit_transcription(audio_file: str) -> dict:
    cfg = load_speech_config()
    request = TranscriptionRequest(audio_url=audio_file, language=cfg.language)
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    speech_config.speech_recognition_language = request.language
    audio_config = speechsdk.audio.AudioConfig(filename=request.audio_url)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    return {
        "service": "Azure AI Speech",
        "language": request.language,
        "recognizer": recognizer.__class__.__name__,
    }
