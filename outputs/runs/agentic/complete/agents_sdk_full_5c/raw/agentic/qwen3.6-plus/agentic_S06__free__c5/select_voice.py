"""Lists or selects a voice for a target locale using ElevenLabs voice library."""

from typing import List, Optional

from speech_client import get_elevenlabs_client, resolve_voice_id
from speech_models import VoiceOption, filter_voices_by_locale, normalize_voices


def list_voices() -> List[VoiceOption]:
    """Fetch all available voices from the ElevenLabs voice library.

    Uses the ElevenLabs voices endpoint (hostname: api.elevenlabs.io)
    to retrieve the full catalog of available voices.
    """
    client = get_elevenlabs_client()
    raw_voices = client.voices.get_all().voices
    raw_list = []
    for v in raw_voices:
        raw_list.append({
            "voice_id": v.voice_id,
            "name": v.name,
            "accent": getattr(v, "accent", ""),
            "description": getattr(v, "description", ""),
            "labels": getattr(v, "labels", {}),
            "preview_url": getattr(v, "preview_url", None),
        })
    return normalize_voices(raw_list)


def select_voice(
    locale: str,
    name_hint: Optional[str] = None,
    gender: Optional[str] = None,
    age: Optional[str] = None,
) -> Optional[VoiceOption]:
    """Select the best matching voice for a target locale from ElevenLabs.

    Filters voices by locale (e.g. 'en-US', 'es-ES', 'fr-FR') and optionally
    by name hint, gender, and age from the ElevenLabs voice metadata.
    Returns the first matching VoiceOption or None.
    """
    all_voices = list_voices()
    locale_matches = filter_voices_by_locale(all_voices, locale)

    candidates = locale_matches
    if gender:
        candidates = _filter_by_label(candidates, "gender", gender)
    if age:
        candidates = _filter_by_label(candidates, "age", age)

    if name_hint:
        named = [v for v in candidates if name_hint.lower() in v.name.lower()]
        if named:
            candidates = named

    if candidates:
        return candidates[0]
    return None


def get_voice_by_id(voice_id: Optional[str] = None) -> VoiceOption:
    """Fetch a specific ElevenLabs voice by its voice_id.

    If no voice_id is provided, the default voice from ELEVENLABS_DEFAULT_VOICE
    or "EXAVITQu4vr4xnSDxMaL" is used.
    """
    client = get_elevenlabs_client()
    vid = resolve_voice_id(voice_id)
    v = client.voices.get(vid)
    raw = {
        "voice_id": v.voice_id,
        "name": v.name,
        "accent": getattr(v, "accent", ""),
        "description": getattr(v, "description", ""),
        "labels": getattr(v, "labels", {}),
        "preview_url": getattr(v, "preview_url", None),
    }
    return normalize_voices([raw])[0]


def _filter_by_label(voices: List[VoiceOption], key: str, value: str) -> List[VoiceOption]:
    """Filter voices whose labels contain the given key/value pair."""
    filtered = []
    for v in voices:
        label_val = v.labels.get(key, "")
        if value.lower() in str(label_val).lower():
            filtered.append(v)
    return filtered
