from __future__ import annotations

from speech_client import (
    default_voice_catalog,
    filter_voices_for_locale,
    pick_voice_for_locale,
)
from speech_models import VoiceOption


def list_voices(locale: str | None = None) -> list[VoiceOption]:
    voices = default_voice_catalog()
    if locale:
        return filter_voices_for_locale(voices, locale)
    return voices


def select_voice(locale: str, preferred_voice: str | None = None) -> VoiceOption:
    return pick_voice_for_locale(locale=locale, preferred_voice=preferred_voice)
