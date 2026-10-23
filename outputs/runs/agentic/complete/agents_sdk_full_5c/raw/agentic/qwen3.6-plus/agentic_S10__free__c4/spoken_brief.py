"""
Generate a spoken brief from model output using ElevenLabs text-to-speech API.

Uses ElevenLabs platform API at api.elevenlabs.io with concrete voice IDs
to convert LLM-generated text into natural-sounding speech audio.
"""

import os
from typing import Optional

import requests


_ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"
_DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice


def get_elevenlabs_api_key() -> str:
    """Retrieve ElevenLabs API key from environment."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable is required. "
            "Set it with your ElevenLabs platform API key."
        )
    return api_key


def generate_spoken_brief(
    text: str,
    voice_id: str = _DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    output_path: Optional[str] = None,
) -> bytes:
    """Generate a spoken brief audio from text using ElevenLabs API.

    Args:
        text: The text content to speak.
        voice_id: ElevenLabs voice identifier (default: Rachel).
        model_id: ElevenLabs TTS model identifier (eleven_multilingual_v2).
        stability: Voice stability (0.0 to 1.0).
        similarity_boost: Voice similarity boost (0.0 to 1.0).
        output_path: Optional file path to save the audio.

    Returns:
        Audio bytes (MP3 format).
    """
    api_key = get_elevenlabs_api_key()

    url = f"{_ELEVENLABS_API_BASE}/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    audio_bytes = response.content

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    return audio_bytes


def generate_spoken_brief_stream(
    text: str,
    voice_id: str = _DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
    output_path: Optional[str] = None,
) -> bytes:
    """Generate spoken brief using ElevenLabs streaming TTS.

    Args:
        text: The text to convert to speech.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model identifier.
        output_path: Optional output file path.

    Returns:
        Audio bytes.
    """
    api_key = get_elevenlabs_api_key()

    url = f"{_ELEVENLABS_API_BASE}/text-to-speech/{voice_id}/stream"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)
    response.raise_for_status()

    audio_chunks = []
    for chunk in response.iter_content(chunk_size=4096):
        audio_chunks.append(chunk)

    audio_bytes = b"".join(audio_chunks)

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    return audio_bytes


def summarize_and_speak(
    llm_output: str,
    max_brief_length: int = 500,
    voice_id: str = _DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
    output_path: Optional[str] = None,
) -> bytes:
    """Create a concise spoken brief from longer LLM output.

    Args:
        llm_output: The full model output text.
        max_brief_length: Maximum characters for the spoken brief.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model identifier.
        output_path: Optional output audio file path.

    Returns:
        Audio bytes of the spoken brief.
    """
    if len(llm_output) > max_brief_length:
        brief_text = llm_output[:max_brief_length].rsplit(".", 1)[0] + "."
        if len(brief_text) < 100:
            brief_text = llm_output[:max_brief_length]
    else:
        brief_text = llm_output

    return generate_spoken_brief(
        text=brief_text,
        voice_id=voice_id,
        model_id=model_id,
        output_path=output_path,
    )


def get_available_voices() -> list:
    """List available ElevenLabs voices.

    Returns:
        List of voice info dicts with voice_id, name, and category.
    """
    api_key = get_elevenlabs_api_key()

    url = f"{_ELEVENLABS_API_BASE}/voices"
    headers = {"xi-api-key": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    voices = []
    for voice in data.get("voices", []):
        voices.append({
            "voice_id": voice["voice_id"],
            "name": voice["name"],
            "category": voice.get("category", "premade"),
        })

    return voices


if __name__ == "__main__":
    sample_text = (
        "Here's your daily AI briefing: The field of artificial intelligence "
        "continues to advance rapidly, with new developments in natural language "
        "processing and computer vision driving innovation across industries."
    )

    try:
        audio = generate_spoken_brief(
            sample_text,
            voice_id=_DEFAULT_VOICE_ID,
            model_id="eleven_multilingual_v2",
            output_path="brief.mp3",
        )
        print(f"Generated {len(audio)} bytes of audio")
    except ValueError as e:
        print(f"Configuration error: {e}")
