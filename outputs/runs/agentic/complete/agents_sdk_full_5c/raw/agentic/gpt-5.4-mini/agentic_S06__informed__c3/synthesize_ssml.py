from __future__ import annotations

from speech_client import synthesize_with_azure
from speech_models import TextToSpeechRequest


def synthesize_ssml(text: str, voice: str, locale: str | None = None, pitch: str | None = None, rate: str | None = None, volume: str | None = None) -> bytes:
    request = TextToSpeechRequest(text=text, voice=voice, locale=locale, ssml=True, pitch=pitch, rate=rate, volume=volume)
    return synthesize_with_azure(request).audio_bytes
