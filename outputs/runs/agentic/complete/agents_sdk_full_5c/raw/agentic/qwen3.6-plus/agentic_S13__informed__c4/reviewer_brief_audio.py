"""
Generate spoken briefs for moderation reviewers.
Provider: ElevenLabs Text to Speech
"""

import os
from typing import Optional

from elevenlabs import ElevenLabs, Voice


DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
}


def _get_elevenlabs_client() -> ElevenLabs:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    return ElevenLabs(api_key=api_key)


def generate_reviewer_brief_audio(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Generate an audio brief for a moderation reviewer using ElevenLabs TTS.

    Args:
        text: The brief text to convert to speech.
        voice_id: ElevenLabs voice identifier.
        model: ElevenLabs TTS model identifier.
        stability: Voice stability (0.0-1.0).
        similarity_boost: Voice similarity boost (0.0-1.0).
        output_path: Optional file path to save the audio file.

    Returns:
        Raw audio bytes (MP3 format).
    """
    client = _get_elevenlabs_client()

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model,
        text=text,
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    )

    audio_bytes = b"".join(chunk for chunk in audio_stream)

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    return audio_bytes


def generate_moderation_brief(
    case_summary: str,
    violation_details: str,
    recommendation: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Generate a structured spoken moderation brief for a reviewer.

    Composes a narrative from case summary, violations, and recommendation,
    then synthesizes it via ElevenLabs.

    Args:
        case_summary: Summary of the moderation case.
        violation_details: Details of the policy violations found.
        recommendation: Reviewer recommendation.
        voice_id: ElevenLabs voice identifier.
        model: ElevenLabs TTS model identifier.
        output_path: Optional file path to save audio.

    Returns:
        Raw audio bytes of the spoken brief.
    """
    brief_text = (
        f"Moderation review brief. "
        f"Case summary: {case_summary}. "
        f"Violation details: {violation_details}. "
        f"Recommendation: {recommendation}. "
        f"End of brief."
    )

    return generate_reviewer_brief_audio(
        text=brief_text,
        voice_id=voice_id,
        model=model,
        output_path=output_path,
    )


def generate_brief_with_custom_voice(
    text: str,
    voice_name: str,
    voice_description: str,
    model: str = DEFAULT_MODEL,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Generate audio using a custom-designed ElevenLabs voice.

    First creates a custom voice via the ElevenLabs API, then synthesizes
    the text using that voice.

    Args:
        text: The brief text to convert to speech.
        voice_name: Name for the custom voice.
        voice_description: Description for voice design.
        model: ElevenLabs TTS model identifier.
        output_path: Optional file path to save audio.

    Returns:
        Raw audio bytes.
    """
    client = _get_elevenlabs_client()

    voice = client.voice_design.create(
        text=voice_description,
        name=voice_name,
    )

    return generate_reviewer_brief_audio(
        text=text,
        voice_id=voice.voice_id,
        model=model,
        output_path=output_path,
    )
