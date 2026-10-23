from __future__ import annotations

from speech_client import available_voices
from speech_models import VoiceSelection, normalize_locale


def select_voice(target_locale: str, preferred_gender: str | None = None) -> VoiceSelection:
    locale = normalize_locale(target_locale)
    voices = available_voices(locale)
    if not voices:
        raise RuntimeError("No Azure voices available")
    if preferred_gender:
        for voice in voices:
            if (voice.gender or "").lower() == preferred_gender.lower():
                return voice
    for voice in voices:
        if normalize_locale(voice.locale) == locale:
            return voice
    return voices[0]
