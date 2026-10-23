from __future__ import annotations

import io
from typing import Optional

import speech_recognition as sr

from speech_models import TranscriptResult

AZURE_SPEECH_STT = "azure-cognitiveservices-speech"


def transcribe_tts_audio(audio_bytes: bytes, language: str = "en-US") -> TranscriptResult:
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language=language)
    return TranscriptResult(text=text, provider=AZURE_SPEECH_STT, confidence=None, metadata={"language": language})
