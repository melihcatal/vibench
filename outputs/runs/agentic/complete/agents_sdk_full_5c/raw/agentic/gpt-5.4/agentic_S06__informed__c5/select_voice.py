from __future__ import annotations

from typing import List, Optional

from speech_client import get_elevenlabs_client
from speech_models import VoiceOption


def list_voices(locale: Optional[str] = None) -> List[VoiceOption]:
    client = get_elevenlabs_client()
    response = client.voices.get_all()
    voices = []
    for voice in response.voices:
        labels = dict(getattr(voice, "labels", {}) or {})
        if locale and labels.get("language") != locale and labels.get("accent") != locale:
            continue
        voices.append(
            VoiceOption(
                voice_id=voice.voice_id,
                name=voice.name,
                labels=labels,
                preview_url=getattr(voice, "preview_url", None),
            )
        )
    return voices


def select_voice(locale: str, preferred_name: Optional[str] = None) -> VoiceOption:
    candidates = list_voices(locale=locale)
    if preferred_name:
        for candidate in candidates:
            if candidate.name.lower() == preferred_name.lower():
                return candidate
    if candidates:
        return candidates[0]
    fallback = list_voices()
    if not fallback:
        raise RuntimeError("No ElevenLabs voices available")
    return fallback[0]
