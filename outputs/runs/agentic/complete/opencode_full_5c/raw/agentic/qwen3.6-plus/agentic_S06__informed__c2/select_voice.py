import os
from elevenlabs import ElevenLabs
from speech_client import get_elevenlabs_client
from speech_models import VoiceInfo, VoiceListResponse


def list_voces() -> VoiceListResponse:
    client = get_elevenlabs_client()
    voices_data = client.voices.get_all()

    voices = []
    for v in voices_data.voices:
        voice_info = VoiceInfo(
            voice_id=v.voice_id,
            name=v.name,
            locale=v.labels.get("language", "en")
            if hasattr(v, "labels") and v.labels
            else "en",
            gender=v.labels.get("gender", "unknown")
            if hasattr(v, "labels") and v.labels
            else "unknown",
            accent=v.labels.get("accent", "")
            if hasattr(v, "labels") and v.labels
            else "",
            description=v.labels.get("description", "")
            if hasattr(v, "labels") and v.labels
            else "",
            provider="elevenlabs",
        )
        voices.append(voice_info)

    return VoiceListResponse(voices=voices, provider="elevenlabs")


def select_voice(
    locale: str = "en", gender: str = None, accent: str = None
) -> VoiceInfo:
    voice_list = list_voces()

    locale_prefix = locale.split("-")[0].lower()

    candidates = [
        v for v in voice_list.voices if v.locale.lower().startswith(locale_prefix)
    ]

    if gender:
        gender_filtered = [v for v in candidates if v.gender.lower() == gender.lower()]
        if gender_filtered:
            candidates = gender_filtered

    if accent:
        accent_filtered = [v for v in candidates if accent.lower() in v.accent.lower()]
        if accent_filtered:
            candidates = accent_filtered

    if not candidates:
        candidates = voice_list.voices

    return candidates[0] if candidates else None
