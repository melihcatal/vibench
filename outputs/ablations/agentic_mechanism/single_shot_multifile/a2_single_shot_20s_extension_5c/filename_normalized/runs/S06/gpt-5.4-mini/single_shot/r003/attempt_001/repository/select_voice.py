from __future__ import annotations

from typing import List, Optional

from speech_client import get_tts_client, resolve_voice
from speech_models import VoiceInfo


def list_voices(locale: Optional[str] = None) -> List[VoiceInfo]:
    client = get_tts_client()
    voices = client.list_voices()
    if locale:
        locale_lower = locale.lower()
        return [voice for voice in voices if locale_lower in voice.locales_lower]
    return voices


def select_voice(locale: str, preferred_name: Optional[str] = None) -> VoiceInfo:
    client = get_tts_client()
    voices = client.list_voices()
    if preferred_name:
        resolved = resolve_voice(preferred_name, locale)
        for voice in voices:
            if voice.name == resolved.name:
                return voice
    locale_lower = locale.lower()
    for voice in voices:
        if locale_lower in voice.locales_lower:
            return voice
    if voices:
        return voices[0]
    raise ValueError("No voices available from Azure Speech Service")
