"""
reviewer_brief_audio.py - Generate spoken briefs for moderation reviewers.

Provider: ElevenLabs Text-to-Speech API
  - SDK: elevenlabs
  - Env: ELEVENLABS_API_KEY
  - API: api.elevenlabs.io
  - Voice: Default professional voice (e.g., "Rachel")
"""

from __future__ import annotations

import io
import os
from typing import Optional, List, Dict, Any

from elevenlabs import ElevenLabs, Voice, VoiceSettings


def get_elevenlabs_client() -> ElevenLabs:
    """Create an ElevenLabs client using the ELEVENLABS_API_KEY environment variable."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    return ElevenLabs(api_key=api_key)


DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - professional female voice
DEFAULT_VOICE_SETTINGS = VoiceSettings(
    stability=0.5,
    similarity_boost=0.75,
    style=0.0,
    use_speaker_boost=True,
)


def generate_reviewer_brief_audio(
    brief_text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    voice_settings: Optional[VoiceSettings] = None,
    model_id: str = "eleven_multilingual_v2",
    client: Optional[ElevenLabs] = None,
) -> bytes:
    """
    Generate a spoken audio brief for a moderation reviewer using ElevenLabs TTS.

    Args:
        brief_text: The text content of the moderation brief to convert to speech.
        voice_id: ElevenLabs voice ID. Defaults to Rachel.
        voice_settings: Optional voice customization settings.
        model_id: ElevenLabs TTS model ID. Defaults to eleven_multilingual_v2.
        client: Optional pre-configured ElevenLabs client.

    Returns:
        Audio bytes in MP3 format.

    Raises:
        ValueError: If brief_text is empty.
    """
    if not brief_text or not brief_text.strip():
        raise ValueError("Brief text must not be empty.")

    if client is None:
        client = get_elevenlabs_client()

    if voice_settings is None:
        voice_settings = DEFAULT_VOICE_SETTINGS

    audio_generator = client.generate(
        text=brief_text,
        voice=Voice(
            voice_id=voice_id,
            settings=voice_settings,
        ),
        model=model_id,
        output_format="mp3_44100_128",
    )

    audio_bytes = b"".join(audio_generator)
    return audio_bytes


def generate_reviewer_brief_audio_stream(
    brief_text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    voice_settings: Optional[VoiceSettings] = None,
    model_id: str = "eleven_multilingual_v2",
    client: Optional[ElevenLabs] = None,
) -> io.BytesIO:
    """
    Generate a spoken audio brief and return as a file-like stream.

    Args:
        brief_text: The text content to convert to speech.
        voice_id: ElevenLabs voice ID.
        voice_settings: Optional voice customization settings.
        model_id: ElevenLabs TTS model ID.
        client: Optional pre-configured ElevenLabs client.

    Returns:
        BytesIO stream containing the MP3 audio.
    """
    audio_bytes = generate_reviewer_brief_audio(
        brief_text,
        voice_id=voice_id,
        voice_settings=voice_settings,
        model_id=model_id,
        client=client,
    )
    return io.BytesIO(audio_bytes)


def generate_batch_reviewer_briefs(
    brief_texts: List[str],
    voice_id: str = DEFAULT_VOICE_ID,
    voice_settings: Optional[VoiceSettings] = None,
    model_id: str = "eleven_multilingual_v2",
    client: Optional[ElevenLabs] = None,
) -> List[bytes]:
    """
    Generate spoken audio briefs for multiple moderation reviews.

    Args:
        brief_texts: List of brief texts to convert to speech.
        voice_id: ElevenLabs voice ID.
        voice_settings: Optional voice customization settings.
        model_id: ElevenLabs TTS model ID.
        client: Optional pre-configured ElevenLabs client.

    Returns:
        List of audio bytes, one per input text.
    """
    if not brief_texts:
        return []

    if client is None:
        client = get_elevenlabs_client()

    if voice_settings is None:
        voice_settings = DEFAULT_VOICE_SETTINGS

    audio_outputs = []
    for text in brief_texts:
        if not text or not text.strip():
            audio_outputs.append(b"")
            continue

        audio_generator = client.generate(
            text=text,
            voice=Voice(
                voice_id=voice_id,
                settings=voice_settings,
            ),
            model=model_id,
            output_format="mp3_44100_128",
        )
        audio_bytes = b"".join(audio_generator)
        audio_outputs.append(audio_bytes)

    return audio_outputs


def build_moderation_brief_text(
    case_id: str,
    category: str,
    severity: int,
    rationale: str,
    recommendation: Optional[str] = None,
) -> str:
    """
    Build a structured text brief for a moderation case.

    Args:
        case_id: The moderation case identifier.
        category: The content safety category.
        severity: The severity score.
        rationale: The moderation rationale.
        recommendation: Optional recommended action.

    Returns:
        Formatted brief text suitable for TTS.
    """
    severity_labels = {0: "safe", 2: "low", 4: "medium", 6: "high"}
    severity_label = severity_labels.get(severity, "unknown")

    brief = (
        f"Moderation brief for case {case_id}. "
        f"Category: {category}. "
        f"Severity level: {severity_label}. "
        f"Rationale: {rationale}."
    )

    if recommendation:
        brief += f" Recommended action: {recommendation}."

    return brief


def generate_case_audio_brief(
    case_id: str,
    category: str,
    severity: int,
    rationale: str,
    recommendation: Optional[str] = None,
    voice_id: str = DEFAULT_VOICE_ID,
    client: Optional[ElevenLabs] = None,
) -> Dict[str, Any]:
    """
    Generate a complete audio brief for a moderation case.

    Args:
        case_id: The moderation case identifier.
        category: The content safety category.
        severity: The severity score.
        rationale: The moderation rationale.
        recommendation: Optional recommended action.
        voice_id: ElevenLabs voice ID.
        client: Optional pre-configured ElevenLabs client.

    Returns:
        Dict with case_id, brief_text, and audio_bytes.
    """
    brief_text = build_moderation_brief_text(
        case_id=case_id,
        category=category,
        severity=severity,
        rationale=rationale,
        recommendation=recommendation,
    )

    audio_bytes = generate_reviewer_brief_audio(
        brief_text=brief_text,
        voice_id=voice_id,
        client=client,
    )

    return {
        "case_id": case_id,
        "brief_text": brief_text,
        "audio_bytes": audio_bytes,
        "voice_id": voice_id,
    }
