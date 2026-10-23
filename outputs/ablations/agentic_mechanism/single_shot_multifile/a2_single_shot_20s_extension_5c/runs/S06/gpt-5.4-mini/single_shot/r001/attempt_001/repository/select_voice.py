from __future__ import annotations

from speech_client import build_tts_client
from speech_models import VoiceSelectionRequest


def select_voice(locale: str, voice_name: str | None = None):
    client = build_tts_client()
    request = VoiceSelectionRequest(locale=locale, voice_name=voice_name)
    if voice_name:
        return client.get_voice(request)
    return client.list_voices(request)
