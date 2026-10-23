from __future__ import annotations

from speech_client import get_tts_client
from speech_models import VoiceSelectionRequest, VoiceSelectionResponse


def select_voice(locale: str | None = None, voice_name: str | None = None) -> VoiceSelectionResponse:
    client = get_tts_client()
    request = VoiceSelectionRequest(locale=locale, voice_name=voice_name)
    return client.select_voice(request)
