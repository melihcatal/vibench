from __future__ import annotations

import os
from pathlib import Path
from typing import Union

import azure.cognitiveservices.speech as speechsdk


def transcribe_qa_audio(audio_source: Union[str, Path]) -> str:
    key = os.getenv("AZURE_SPEECH_KEY", "")
    region = os.getenv("AZURE_SPEECH_REGION", "")
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename=str(audio_source))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once_async().get()
    if result.reason != speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError(f"Azure Speech transcription failed: {result.reason}")
    return result.text
