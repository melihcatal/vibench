"""
[SAME-SCENARIO] select_voice.py
Lists or selects a voice for a target locale using ElevenLabs TTS API.
"""
from typing import Optional, List, Dict, Any
from elevenlabs import ElevenLabs
from speech_models import VoiceInfo, VoiceListResponse, VoiceGender
from speech_client import (
    get_elevenlabs_client,
    elevenlabs_voice_to_voice_info,
)


def list_voices(
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> VoiceListResponse:
    """
    List all available voices from ElevenLabs.

    Args:
        api_key: Optional ElevenLabs API key.
        client: Optional pre-built ElevenLabs client.

    Returns:
        VoiceListResponse containing normalized voice information.
    """
    if client is None:
        client = get_elevenlabs_client(api_key)

    voices_data = client.voices.get_all()
    voice_list = voices_data.voices if hasattr(voices_data, "voices") else []

    normalized_voices = []
    for v in voice_list:
        voice_dict = {
            "voice_id": v.voice_id,
            "name": v.name,
            "description": v.description or "",
            "category": v.category if hasattr(v, "category") else "premade",
            "labels": {},
        }
        if hasattr(v, "labels") and v.labels:
            voice_dict["labels"] = v.labels
        normalized_voices.append(elevenlabs_voice_to_voice_info(voice_dict))

    return VoiceListResponse(
        voices=normalized_voices,
        total_count=len(normalized_voices),
    )


def select_voice_for_locale(
    locale: str,
    gender: Optional[VoiceGender] = None,
    category: Optional[str] = None,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> Optional[VoiceInfo]:
    """
    Select the best matching voice for a target locale from ElevenLabs.

    Args:
        locale: Target locale code (e.g., "en", "en-US", "fr", "ja").
        gender: Optional voice gender filter.
        category: Optional voice category filter (e.g., "premade", "cloned").
        api_key: Optional ElevenLabs API key.
        client: Optional pre-built ElevenLabs client.

    Returns:
        VoiceInfo for the best matching voice, or None if no match found.
    """
    voice_list = list_voices(api_key=api_key, client=client)
    locale_base = locale.split("-")[0].lower()

    candidates = []
    for voice in voice_list.voices:
        voice_locale = voice.language_code.lower().split("-")[0]
        if voice_locale != locale_base:
            continue

        if gender and voice.gender != gender:
            continue

        if category and voice.category != category:
            continue

        candidates.append(voice)

    if candidates:
        return candidates[0]
    return None


def get_voice_by_id(
    voice_id: str,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> Optional[VoiceInfo]:
    """
    Retrieve a specific voice by its ElevenLabs voice_id.

    Args:
        voice_id: The ElevenLabs voice ID to look up.
        api_key: Optional ElevenLabs API key.
        client: Optional pre-built ElevenLabs client.

    Returns:
        VoiceInfo for the specified voice, or None if not found.
    """
    if client is None:
        client = get_elevenlabs_client(api_key)

    voice_list = list_voices(client=client)
    for voice in voice_list.voices:
        if voice.voice_id == voice_id:
            return voice
    return None


def get_voice_id_by_name(
    name: str,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> Optional[str]:
    """
    Get the ElevenLabs voice_id for a given voice name.

    Args:
        name: The voice name to search for (case-insensitive).
        api_key: Optional ElevenLabs API key.
        client: Optional pre-built ElevenLabs client.

    Returns:
        The ElevenLabs voice_id string, or None if not found.
    """
    voice_list = list_voices(api_key=api_key, client=client)
    name_lower = name.lower()
    for voice in voice_list.voices:
        if voice.name.lower() == name_lower:
            return voice.voice_id
    return None


if __name__ == "__main__":
    voices = list_voices()
    print(f"Found {voices.total_count} voices in ElevenLabs:")
    for v in voices.voices:
        print(f"  - {v.name} ({v.voice_id}) [{v.language_code}]")

    selected = select_voice_for_locale("en", gender=VoiceGender.FEMALE)
    if selected:
        print(f"\nSelected voice for 'en': {selected.name} ({selected.voice_id})")
