from __future__ import annotations

from speech_client import build_tts_client
from speech_models import SsmlRequest, normalize_ssml_request


def synthesize_ssml(ssml: str, voice: str | None = None, locale: str | None = None, pitch: str | None = None, rate: str | None = None) -> bytes:
    client = build_tts_client()
    request = normalize_ssml_request(SsmlRequest(ssml=ssml, voice=voice, locale=locale, pitch=pitch, rate=rate))
    response = client.synthesize_ssml(request)
    return response.audio
