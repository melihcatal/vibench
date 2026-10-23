from __future__ import annotations

from speech_client import synthesize_request
from speech_models import TextToSpeechRequest, normalize_text


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None) -> bytes:
    request = TextToSpeechRequest(text=normalize_text(text), voice=voice, locale=locale, output_format="mp3", ssml=False)
    return synthesize_request(request).audio_bytes
