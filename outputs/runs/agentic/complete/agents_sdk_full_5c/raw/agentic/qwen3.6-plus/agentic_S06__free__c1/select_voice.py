"""
select_voice.py - Lists or selects a voice for a target locale using ElevenLabs.

Provider: ElevenLabs (https://api.elevenlabs.io)
API Endpoint: GET /v1/voices
SDK: elevenlabs Python package
"""

from typing import List, Optional

from elevenlabs import ElevenLabs

from speech_client import get_elevenlabs_client
from speech_models import VoiceInfo, normalize_voice_list


# ElevenLabs API endpoint for listing voices
ELEVENLABS_VOICES_ENDPOINT = "https://api.elevenlabs.io/v1/voices"

# Well-known ElevenLabs voice IDs
ELEVENLABS_VOICE_RACHEL = "21m00Tcm4TlvDq8ikWAM"
ELEVENLABS_VOICE_ANTONI = "ErXwobaYiN019PkySvjV"
ELEVENLABS_VOICE_BELLA = "EXAVITQu4vr4xnSDxMaL"
ELEVENLABS_VOICE_JOSH = "TxGEqnHWrfWFTfGW9XjX"
ELEVENLABS_VOICE_ARNOLD = "VR6AewLTigWG4xSOukaG"
ELEVENLABS_VOICE_CHARLOTTE = "XB0fDUnXU5powFXDhCwa"


def list_voices(
    api_key: Optional[str] = None,
    show_all: bool = True,
) -> List[VoiceInfo]:
    """List all available voices from ElevenLabs.

    Args:
        api_key: Optional explicit API key override.
        show_all: If True, include cloned and custom voices.

    Returns:
        List of VoiceInfo objects for all available voices.
    """
    client = get_elevenlabs_client(api_key=api_key)
    voices_response = client.voices.get_all()
    voices = list(voices_response.voices) if voices_response.voices else []
    return normalize_voice_list(voices)


def select_voice_for_locale(
    target_locale: str,
    category: Optional[str] = "premade",
    api_key: Optional[str] = None,
) -> Optional[VoiceInfo]:
    """Select the best voice for a target locale from ElevenLabs.

    Searches ElevenLabs voices filtered by locale and category,
    returning the first matching voice.

    Supported locale prefixes:
        'en' - English (US/UK/AU)
        'es' - Spanish
        'fr' - French
        'de' - German
        'it' - Italian
        'pt' - Portuguese
        'pl' - Polish
        'ja' - Japanese
        'ko' - Korean
        'zh' - Chinese
        'ar' - Arabic
        'hi' - Hindi
        'ru' - Russian
        'tr' - Turkish

    Args:
        target_locale: BCP-47 locale string (e.g., 'en-US', 'es-ES', 'ja-JP').
        category: Voice category filter (default: 'premade').
        api_key: Optional explicit API key override.

    Returns:
        Best matching VoiceInfo or None if no match found.
    """
    voices = list_voices(api_key=api_key, show_all=True)

    # Filter by locale
    locale_matches = [
        v for v in voices if v.matches_locale(target_locale)
    ]

    if not locale_matches:
        return None

    # Prefer premade voices if category specified
    if category:
        category_matches = [
            v for v in locale_matches
            if v.category.lower() == category.lower()
        ]
        if category_matches:
            return category_matches[0]

    return locale_matches[0]


def get_voice_by_id(
    voice_id: str,
    api_key: Optional[str] = None,
) -> VoiceInfo:
    """Retrieve a specific voice by its ElevenLabs voice ID.

    Args:
        voice_id: ElevenLabs voice identifier.
        api_key: Optional explicit API key override.

    Returns:
        VoiceInfo for the specified voice.

    Raises:
        ValueError: If the voice ID is not found.
    """
    client = get_elevenlabs_client(api_key=api_key)
    voice = client.voices.get(voice_id=voice_id)
    if not voice:
        raise ValueError(f"ElevenLabs voice not found: {voice_id}")
    return VoiceInfo.from_elevenlabs_voice(voice)


def get_default_voice_for_locale(locale: str) -> str:
    """Return a well-known ElevenLabs voice ID for a given locale.

    Args:
        locale: BCP-47 locale string.

    Returns:
        ElevenLabs voice ID string.
    """
    locale_prefix = locale.split("-")[0].lower()
    default_map = {
        "en": ELEVENLABS_VOICE_RACHEL,
        "es": ELEVENLABS_VOICE_ANTONI,
        "fr": ELEVENLABS_VOICE_BELLA,
        "de": ELEVENLABS_VOICE_JOSH,
        "it": ELEVENLABS_VOICE_CHARLOTTE,
    }
    return default_map.get(locale_prefix, ELEVENLABS_VOICE_RACHEL)


def filter_voices_by_gender(
    voices: List[VoiceInfo],
    gender: str,
) -> List[VoiceInfo]:
    """Filter voices by gender label.

    ElevenLabs voices may include a 'gender' label in their metadata.

    Args:
        voices: List of VoiceInfo objects.
        gender: Target gender ('male' or 'female').

    Returns:
        Filtered list of voices.
    """
    return [
        v for v in voices
        if v.labels.get("gender", "").lower() == gender.lower()
    ]


def select_voice_interactive(
    target_locale: str = "en-US",
    gender: Optional[str] = None,
    category: str = "premade",
    api_key: Optional[str] = None,
) -> VoiceInfo:
    """Select a voice with additional filtering options.

    Args:
        target_locale: BCP-47 locale string.
        gender: Optional gender filter ('male' or 'female').
        category: Voice category filter.
        api_key: Optional explicit API key override.

    Returns:
        Selected VoiceInfo.
    """
    voices = list_voices(api_key=api_key, show_all=True)
    locale_matches = [v for v in voices if v.matches_locale(target_locale)]

    if category:
        locale_matches = [
            v for v in locale_matches
            if v.category.lower() == category.lower()
        ]

    if gender:
        locale_matches = filter_voices_by_gender(locale_matches, gender)

    if not locale_matches:
        raise ValueError(
            f"No ElevenLabs voices found for locale={target_locale}, "
            f"gender={gender}, category={category}"
        )

    return locale_matches[0]


if __name__ == "__main__":
    voices = list_voices()
    print(f"Found {len(voices)} ElevenLabs voices:")
    for v in voices[:5]:
        print(f"  - {v.name} ({v.voice_id}) - {v.language} [{v.category}]")

    selected = select_voice_for_locale("en-US")
    if selected:
        print(f"\nSelected voice for en-US: {selected.name} ({selected.voice_id})")
