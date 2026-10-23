from __future__ import annotations

from typing import Optional

from speech_client import list_voices
from speech_models import VoiceInfo, select_voice_for_locale


def select_voice(locale: str, preferred_name: Optional[str] = None) -> VoiceInfo:
    voices = list_voices(locale)
    if preferred_name:
        for voice in voices:
            if voice.name == preferred_name:
                return voice
    selected = select_voice_for_locale(voices, locale)
    if selected is None:
        raise RuntimeError(f"No Azure Speech voices available for locale: {locale}")
    return selected
