from __future__ import annotations

from speech_client import synthesize_request
from speech_models import TextToSpeechRequest, normalize_ssml


def synthesize_ssml(ssml: str, voice: str | None = None, locale: str | None = None, prosody: dict | None = None) -> bytes:
    request = TextToSpeechRequest(text=normalize_ssml(ssml), voice=voice, locale=locale, output_format="mp3", ssml=True, prosody=prosody)
    return synthesize_request(request).audio_bytes
