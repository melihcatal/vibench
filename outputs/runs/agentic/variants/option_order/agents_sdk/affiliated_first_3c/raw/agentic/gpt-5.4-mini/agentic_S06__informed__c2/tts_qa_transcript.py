from __future__ import annotations

import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config


def transcribe_audio_file(audio_path: str | Path) -> str:
    speech_config = get_speech_config()
    audio_input = speechsdk.audio.AudioConfig(filename=str(audio_path))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = recognizer.recognize_once_async().get()
    if result.reason != speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError(f"Azure Speech transcription failed: {result.reason}")
    return result.text
