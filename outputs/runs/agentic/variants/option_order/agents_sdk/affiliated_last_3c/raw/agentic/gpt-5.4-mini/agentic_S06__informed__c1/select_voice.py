from __future__ import annotations

from speech_client import get_polly_client
from speech_models import VoiceSelection, voice_matches_locale


def select_voice(locale: str | None = None, preferred_voice_id: str | None = None) -> VoiceSelection:
    client = get_polly_client()
    voices = client.describe_voices().get("Voices", [])
    selected = None
    if preferred_voice_id:
        selected = next((v for v in voices if v.get("Id") == preferred_voice_id), None)
    if selected is None and locale:
        selected = next((v for v in voices if voice_matches_locale(v, locale)), None)
    if selected is None:
        selected = voices[0] if voices else None
    selected_voice_id = selected.get("Id") if selected else None
    return VoiceSelection(voices=voices, locale=locale, selected_voice_id=selected_voice_id)
