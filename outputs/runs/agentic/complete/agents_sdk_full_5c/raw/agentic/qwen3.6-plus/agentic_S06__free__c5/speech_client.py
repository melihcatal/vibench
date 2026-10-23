"""Local configuration and client helper utilities for Text-to-Speech."""

import os
from typing import Optional

from elevenlabs import ElevenLabs


def get_elevenlabs_client(api_key: Optional[str] = None) -> ElevenLabs:
    """Create and return an ElevenLabs client using the provided or env API key."""
    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable or explicit api_key is required")
    return ElevenLabs(api_key=key)


def get_output_dir(output_dir: Optional[str] = None) -> str:
    """Resolve the output directory for saving audio files."""
    directory = output_dir or os.environ.get("TTS_OUTPUT_DIR", "./output")
    os.makedirs(directory, exist_ok=True)
    return directory


def resolve_voice_id(voice_id: Optional[str]) -> str:
    """Return a default ElevenLabs voice ID if none provided."""
    return voice_id or os.environ.get("ELEVENLABS_DEFAULT_VOICE", "EXAVITQu4vr4xnSDxMaL")


def resolve_model_id(model_id: Optional[str]) -> str:
    """Return a default ElevenLabs model ID if none provided."""
    return model_id or os.environ.get("ELEVENLABS_DEFAULT_MODEL", "eleven_multilingual_v2")


def configure_speech_settings(
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
    style: Optional[float] = None,
    use_speaker_boost: Optional[bool] = None,
) -> dict:
    """Build a settings dict compatible with ElevenLabs voice settings."""
    settings = {}
    if stability is not None:
        settings["stability"] = float(stability)
    if similarity_boost is not None:
        settings["similarity_boost"] = float(similarity_boost)
    if style is not None:
        settings["style"] = float(style)
    if use_speaker_boost is not None:
        settings["use_speaker_boost"] = bool(use_speaker_boost)
    return settings


def resolve_audio_format(output_format: Optional[str]) -> str:
    """Resolve and validate the output audio format."""
    supported = {"mp3_22050_32", "mp3_44100_32", "mp3_44100_64", "mp3_44100_96", "mp3_44100_128", "mp3_44100_192",
                 "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100", "ulaw_8000"}
    fmt = output_format or os.environ.get("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128")
    if fmt not in supported:
        raise ValueError(f"Unsupported ElevenLabs output format: {fmt}")
    return fmt
