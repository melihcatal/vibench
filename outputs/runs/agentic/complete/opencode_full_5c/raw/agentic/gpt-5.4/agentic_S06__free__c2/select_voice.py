from __future__ import annotations

from speech_client import choose_voice, list_voices
from speech_models import VoiceOption, normalize_locale


def select_voice(locale: str, preferred_voice: str | None = None) -> VoiceOption:
    return choose_voice(
        locale=normalize_locale(locale), preferred_voice=preferred_voice
    )


def list_locale_voices(locale: str) -> list[VoiceOption]:
    return list_voices(locale=normalize_locale(locale))
