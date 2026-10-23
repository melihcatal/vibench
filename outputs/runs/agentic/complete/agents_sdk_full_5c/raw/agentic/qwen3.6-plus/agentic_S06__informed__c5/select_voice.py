"""List or select a voice for a target locale using ElevenLabs Text to Speech."""

from typing import Optional

from elevenlabs import ElevenLabs

from speech_client import (
    create_elevenlabs_client,
    normalize_voice_list_response,
)
from speech_models import VoiceInfo, VoiceSelectionResult


def _raw_to_voice_info(voice) -> VoiceInfo:
    """Convert a raw ElevenLabs voice object to a normalized VoiceInfo."""
    labels = {}
    raw_labels = getattr(voice, "labels", None)
    if raw_labels:
        if isinstance(raw_labels, dict):
            labels = raw_labels
        elif hasattr(raw_labels, "__dict__"):
            labels = {k: str(v) for k, v in vars(raw_labels).items()}

    locale = labels.get("accent", "") or labels.get("accent", "")
    gender = labels.get("gender", "") or labels.get("description", "")

    return VoiceInfo(
        voice_id=voice.voice_id,
        name=voice.name,
        category=getattr(voice, "category", ""),
        locale=locale,
        gender=gender,
        labels=labels,
        preview_url=getattr(voice, "preview_url", None),
    )


def list_voices(
    *,
    client: Optional[ElevenLabs] = None,
) -> VoiceSelectionResult:
    """List all available ElevenLabs voices and normalize the response.

    Args:
        client: Optional pre-configured ElevenLabs client instance.

    Returns:
        VoiceSelectionResult with all available voices.
    """
    if client is None:
        client = create_elevenlabs_client()

    raw_voices = client.voices.get_all()
    voices = [_raw_to_voice_info(v) for v in raw_voices.voices]

    return VoiceSelectionResult(
        voices=voices,
        total_count=len(voices),
    )


def select_voice_for_locale(
    target_locale: str,
    *,
    client: Optional[ElevenLabs] = None,
    preferred_name: Optional[str] = None,
) -> VoiceSelectionResult:
    """Select a voice that best matches a target locale using ElevenLabs.

    Queries the ElevenLabs voices API and filters for voices whose locale
    or accent label matches the target locale. If a preferred voice name
    is given, it takes priority when it also matches the locale.

    Args:
        target_locale: Target locale code (e.g., 'en-US', 'es-ES', 'ja-JP').
        client: Optional pre-configured ElevenLabs client.
        preferred_name: Optional preferred voice name to prioritize.

    Returns:
        VoiceSelectionResult with matching voices and a selected voice if found.
    """
    result = list_voices(client=client)

    matching = []
    for voice in result.voices:
        if voice.matches_locale(target_locale):
            matching.append(voice)

    selected = None
    if preferred_name:
        for v in matching:
            if preferred_name.lower() in v.name.lower():
                selected = v
                break

    if selected is None and matching:
        selected = matching[0]

    return VoiceSelectionResult(
        voices=matching,
        selected_voice=selected,
        total_count=len(matching),
    )
