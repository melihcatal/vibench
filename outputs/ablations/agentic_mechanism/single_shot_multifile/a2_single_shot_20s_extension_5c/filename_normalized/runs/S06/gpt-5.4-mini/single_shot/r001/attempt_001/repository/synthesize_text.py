from __future__ import annotations

from speech_client import build_tts_client
from speech_models import TextToSpeechRequest, normalize_text_request


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None) -> bytes:
    client = build_tts_client()
    request = normalize_text_request(TextToSpeechRequest(text=text, voice=voice, locale=locale))
    response = client.synthesize_text(request)
    return response.audio
