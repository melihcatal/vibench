"""
Generate a spoken brief from the model output.

Provider: ElevenLabs Text to Speech
SDK: requests (REST interface to ElevenLabs API)
Auth: ELEVENLABS_API_KEY
Endpoint: api.elevenlabs.io/v1/text-to-speech
"""

import os
from typing import Any, Dict, Optional

import requests

ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"

DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - default ElevenLabs voice
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def _resolve_elevenlabs_config() -> Dict[str, str]:
    """Resolve ElevenLabs API configuration from environment variables."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ELEVENLABS_API_KEY is required for ElevenLabs Text-to-Speech integration"
        )
    return {"api_key": api_key}


def text_to_speech(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
    output_format: str = "mp3_44100_128",
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
) -> bytes:
    """
    Convert text to speech audio using the ElevenLabs API.

    Provider: ElevenLabs Text to Speech
    Endpoint: api.elevenlabs.io/v1/text-to-speech/{voice_id}
    Voice IDs: ElevenLabs-provided voice identifiers (e.g., 21m00Tcm4TlvDq8ikWAM)
    Model IDs: eleven_multilingual_v2, eleven_monolingual_v1, etc.

    Args:
        text: The text to convert to speech.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model identifier.
        output_format: Audio output format (e.g., mp3_44100_128, pcm_16000).
        stability: Voice stability (0.0 to 1.0).
        similarity_boost: Voice similarity boost (0.0 to 1.0).

    Returns:
        Raw audio bytes in the specified format.
    """
    config = _resolve_elevenlabs_config()
    url = f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": config["api_key"],
        "Content-Type": "application/json",
    }

    voice_settings: Dict[str, Any] = {}
    if stability is not None:
        voice_settings["stability"] = stability
    if similarity_boost is not None:
        voice_settings["similarity_boost"] = similarity_boost

    payload: Dict[str, Any] = {
        "text": text,
        "model_id": model_id,
        "output_format": output_format,
    }
    if voice_settings:
        payload["voice_settings"] = voice_settings

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.content


def generate_spoken_brief(
    model_output: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
    max_chars: int = 5000,
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a spoken audio brief from LLM model output via ElevenLabs.

    Args:
        model_output: The text output from a hosted LLM.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model ID (e.g., eleven_multilingual_v2).
        max_chars: Maximum characters to include in the audio brief.
        output_format: Audio format for the output.
        stability: Voice stability parameter.
        similarity_boost: Voice similarity boost parameter.
        output_path: Optional file path to save the audio file.

    Returns:
        Dictionary containing the audio bytes and metadata.
    """
    truncated = model_output[:max_chars]
    if len(model_output) > max_chars:
        truncated += "..."

    audio_bytes = text_to_speech(
        text=truncated,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost,
    )

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    return {
        "audio_bytes": audio_bytes,
        "text_truncated": truncated,
        "voice_id": voice_id,
        "model_id": model_id,
        "output_format": output_format,
        "file_size": len(audio_bytes),
        "output_path": output_path,
        "provider": "elevenlabs",
    }
