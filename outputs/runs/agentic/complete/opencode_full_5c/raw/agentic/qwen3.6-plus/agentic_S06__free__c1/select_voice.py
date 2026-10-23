from __future__ import annotations

from speech_client import create_openai_client, VOICE_LOCALE_MAP, SUPPORTED_VOICES
from speech_models import VoiceInfo


def list_voices(api_key: str | None = None) -> list[VoiceInfo]:
    client = create_openai_client(api_key=api_key)
    voices = []
    for voice_id in SUPPORTED_VOICES:
        info = VOICE_LOCALE_MAP.get(voice_id, {})
        voices.append(
            VoiceInfo(
                id=voice_id,
                locale=info.get("locale", "en-US"),
                gender=info.get("gender", "neutral"),
                accent=info.get("accent", "american"),
                sample_rate=24000,
            )
        )
    return voices


def select_voice(
    locale: str = "en-US",
    gender: str | None = None,
    accent: str | None = None,
    api_key: str | None = None,
) -> VoiceInfo:
    voices = list_voices(api_key=api_key)
    locale_lower = locale.lower()

    candidates = [v for v in voices if v.locale.lower() == locale_lower]

    if not candidates and locale_lower.startswith("en"):
        candidates = voices

    if gender:
        gender_lower = gender.lower()
        gender_matched = [v for v in candidates if v.gender.lower() == gender_lower]
        if gender_matched:
            candidates = gender_matched

    if accent:
        accent_lower = accent.lower()
        accent_matched = [v for v in candidates if v.accent.lower() == accent_lower]
        if accent_matched:
            candidates = accent_matched

    if not candidates:
        candidates = voices

    selected = candidates[0]
    return selected
