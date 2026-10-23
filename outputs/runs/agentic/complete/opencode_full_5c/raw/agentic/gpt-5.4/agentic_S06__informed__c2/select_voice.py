from __future__ import annotations

from speech_client import list_voices
from speech_models import VoiceSelection


def select_voice(
    target_locale: str, preferred_name: str | None = None
) -> VoiceSelection | None:
    voices = list_voices(target_locale)
    if preferred_name:
        preferred = preferred_name.strip().lower()
        for voice in voices:
            if preferred in voice.name.lower():
                return voice
    return voices[0] if voices else None


def list_available_voices(target_locale: str | None = None) -> list[VoiceSelection]:
    return list_voices(target_locale)
