from __future__ import annotations

from typing import List, Optional

from speech_client import get_tts_client, resolve_voice_id
from speech_models import VoiceSelection, normalize_locale


def list_voices(locale: Optional[str] = None) -> List[VoiceSelection]:
    client = get_tts_client()
    target = normalize_locale(locale) if locale else None
    results: List[VoiceSelection] = []
    for voice in client.voices.get_all().voices:
        labels = getattr(voice, "labels", {}) or {}
        voice_locale = labels.get("accent") or labels.get("language") or target or "und"
        if target and normalize_locale(voice_locale) != target:
            continue
        results.append(
            VoiceSelection(
                locale=normalize_locale(voice_locale),
                voice_id=getattr(voice, "voice_id", None),
                name=getattr(voice, "name", None),
                gender=labels.get("gender"),
            )
        )
    return results


def select_voice(
    locale: str, preferred_voice_id: Optional[str] = None
) -> VoiceSelection:
    if preferred_voice_id:
        return VoiceSelection(
            locale=normalize_locale(locale), voice_id=preferred_voice_id
        )
    voices = list_voices(locale)
    if voices:
        return voices[0]
    return VoiceSelection(locale=normalize_locale(locale), voice_id=resolve_voice_id())
