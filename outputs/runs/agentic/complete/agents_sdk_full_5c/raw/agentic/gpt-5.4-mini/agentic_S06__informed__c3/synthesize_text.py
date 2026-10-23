from __future__ import annotations

from speech_client import synthesize_with_azure
from speech_models import TextToSpeechRequest


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None) -> bytes:
    request = TextToSpeechRequest(text=text, voice=voice, locale=locale, ssml=False)
    return synthesize_with_azure(request).audio_bytes
