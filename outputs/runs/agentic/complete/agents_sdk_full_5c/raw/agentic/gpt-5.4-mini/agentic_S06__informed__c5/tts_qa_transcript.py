from __future__ import annotations

import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk


SPEECH_KEY = os.environ["AZURE_SPEECH_KEY"]
SPEECH_REGION = os.environ["AZURE_SPEECH_REGION"]


def transcribe_sample(audio_path: str | Path) -> str:
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=str(audio_path))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once_async().get()
    return result.text
