from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import azure.cognitiveservices.speech as speechsdk


def transcribe_tts_sample(audio_path: str | Path, locale: Optional[str] = None) -> str:
    key = os.environ.get("AZURE_SPEECH_KEY", "")
    region = os.environ.get("AZURE_SPEECH_REGION", "")
    if not key or not region:
        raise EnvironmentError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    if locale:
        speech_config.speech_recognition_language = locale
    audio_config = speechsdk.AudioConfig(filename=str(audio_path))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once_async().get()
    if result.reason != speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError(f"Speech recognition failed: {result.reason}")
    return result.text
