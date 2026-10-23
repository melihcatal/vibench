"""
Generate a spoken brief from model output using ElevenLabs Text-to-Speech API.
Provider: ElevenLabs (elevenlabs SDK, ELEVENLABS_API_KEY)
"""

import os
from typing import Optional, Union, BinaryIO
import io

import elevenlabs


DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def _get_elevenlabs_client() -> elevenlabs.ElevenLabs:
    """Create and return an authenticated ElevenLabs client."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    return elevenlabs.ElevenLabs(api_key=api_key)


def generate_spoken_brief(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    clarity: float = 0.75,
) -> bytes:
    """
    Generate a spoken audio brief from text using ElevenLabs TTS API.

    Args:
        text: The text to convert to speech.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model identifier.
        output_format: Audio output format.
        stability: Voice stability (0.0 to 1.0).
        clarity: Voice clarity/similarity boost (0.0 to 1.0).

    Returns:
        Audio bytes in the specified format.
    """
    client = _get_elevenlabs_client()

    audio = client.generate(
        text=text,
        voice=voice_id,
        model=model_id,
        output_format=output_format,
        voice_settings=elevenlabs.VoiceSettings(
            stability=stability,
            similarity_boost=clarity,
        ),
    )

    audio_bytes = b"".join(audio)
    return audio_bytes


def generate_spoken_brief_to_file(
    text: str,
    filepath: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
) -> str:
    """
    Generate spoken brief and save to file.

    Args:
        text: The text to convert to speech.
        filepath: Output audio file path.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model identifier.

    Returns:
        The filepath of the saved audio file.
    """
    audio_bytes = generate_spoken_brief(text, voice_id, model_id)
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    return filepath


def generate_spoken_brief_to_stream(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
) -> BinaryIO:
    """
    Generate spoken brief and return as a file-like stream.

    Args:
        text: The text to convert to speech.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model identifier.

    Returns:
        BytesIO stream containing the audio data.
    """
    audio_bytes = generate_spoken_brief(text, voice_id, model_id)
    return io.BytesIO(audio_bytes)
