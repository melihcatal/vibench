from __future__ import annotations

from speech_client import synthesize_text_request
from speech_models import TTSRequest


def synthesize_text(text: str, voice_name: str | None = None, locale: str | None = None) -> bytes:
    response = synthesize_text_request(TTSRequest(text=text, voice_name=voice_name, locale=locale))
    return response.audio
