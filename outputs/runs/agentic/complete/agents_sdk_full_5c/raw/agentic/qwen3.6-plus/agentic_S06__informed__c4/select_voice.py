"""
List or select a voice for a target locale using ElevenLabs Text to Speech.

Provider: ElevenLabs Text to Speech
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

from typing import Optional, List

from elevenlabs import ElevenLabs

from speech_client import get_elevenlabs_client
from speech_models import VoiceInfo, VoiceList, parse_elevenlabs_voices_list


def list_voices(
    api_key: Optional[str] = None,
) -> VoiceList:
    """List all available voices from ElevenLabs.

    Args:
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env var.

    Returns:
        VoiceList with all available voices.
    """
    client: ElevenLabs = get_elevenlabs_client(api_key)
    response = client.voices.get_all()

    # Convert response to dict format for parsing
    voices_data = {
        "voices": [
            {
                "voice_id": v.voice_id,
                "name": v.name,
                "category": v.category,
                "description": v.description,
                "labels": v.labels or {},
                "preview_url": v.preview_url or "",
            }
            for v in response.voices
        ]
    }

    return parse_elevenlabs_voices_list(voices_data)


def select_voice_for_locale(
    locale: str,
    api_key: Optional[str] = None,
    preferred_gender: Optional[str] = None,
) -> Optional[VoiceInfo]:
    """Select a voice matching a target locale.

    Args:
        locale: Target locale code (e.g. 'en-US', 'es-ES', 'ja-JP').
        api_key: ElevenLabs API key.
        preferred_gender: Optional gender preference ('male', 'female').

    Returns:
        Best matching VoiceInfo or None.
    """
    all_voices = list_voices(api_key)
    matched = all_voices.filter_by_locale(locale)

    if not matched.voices:
        return None

    if preferred_gender:
        for voice in matched.voices:
            if voice.gender.lower() == preferred_gender.lower():
                return voice

    return matched.voices[0]


def get_voice_by_id(
    voice_id: str,
    api_key: Optional[str] = None,
) -> Optional[VoiceInfo]:
    """Get a specific voice by its ElevenLabs voice ID.

    Args:
        voice_id: ElevenLabs voice identifier (e.g. 'EXAVITQu4vr4xnSDxMaL').
        api_key: ElevenLabs API key.

    Returns:
        VoiceInfo or None if not found.
    """
    client: ElevenLabs = get_elevenlabs_client(api_key)
    try:
        voice = client.voices.get(voice_id)
        return VoiceInfo(
            voice_id=voice.voice_id,
            name=voice.name,
            category=voice.category,
            description=voice.description,
            labels=voice.labels or {},
            locale=(voice.labels or {}).get("language", ""),
            gender=(voice.labels or {}).get("gender", ""),
            preview_url=voice.preview_url or "",
        )
    except Exception:
        return None


def get_recommended_voice(
    language: str = "en",
    style: str = "narration",
    api_key: Optional[str] = None,
) -> str:
    """Get a recommended ElevenLabs voice ID for a language and style.

    Args:
        language: Language code (e.g. 'en', 'es', 'fr').
        style: Use case style (e.g. 'narration', 'conversational', 'news').
        api_key: ElevenLabs API key.

    Returns:
        Voice ID string.
    """
    voice_map = {
        ("en", "narration"): "EXAVITQu4vr4xnSDxMaL",
        ("en", "conversational"): "21m00Tcm4TlvDq8ikWAM",
        ("en", "news"): "AZnzlk1XvdvUeBnXmlld",
        ("es", "narration"): "EXAVITQu4vr4xnSDxMaL",
        ("fr", "narration"): "EXAVITQu4vr4xnSDxMaL",
        ("ja", "narration"): "EXAVITQu4vr4xnSDxMaL",
    }

    key = (language.lower(), style.lower())
    if key in voice_map:
        return voice_map[key]

    # Fallback: search for matching locale
    voice = select_voice_for_locale(language, api_key)
    if voice:
        return voice.voice_id

    # Ultimate fallback to default Rachel voice
    return "EXAVITQu4vr4xnSDxMaL"
