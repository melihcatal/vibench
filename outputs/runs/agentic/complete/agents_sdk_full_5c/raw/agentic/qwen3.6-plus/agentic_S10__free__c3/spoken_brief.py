"""
Generates a spoken brief from model output using OpenAI Text-to-Speech API.

Provider: OpenAI (api.openai.com)
Model family: tts-1 / tts-1-hd
"""

import base64
from typing import Optional

from model_client import get_sync_client, DEFAULT_TTS_MODEL
from model_models import (
    SpokenBriefRequest,
    SpokenBriefResponse,
)

OPENAI_API_HOST = "api.openai.com"
OPENAI_TTS_MODEL = "tts-1"

# Available OpenAI TTS voices
OPENAI_TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def generate_spoken_brief(
    request: SpokenBriefRequest,
    model: Optional[str] = None,
    speed: float = 1.0,
) -> SpokenBriefResponse:
    """
    Generate a spoken audio brief from text using OpenAI's tts-1 model
    hosted on api.openai.com.

    Args:
        request: SpokenBriefRequest with text and voice parameters.
        model: Optional explicit OpenAI TTS model identifier
               (tts-1 or tts-1-hd for higher quality).
        speed: Speech speed multiplier (0.25 to 4.0).

    Returns:
        SpokenBriefResponse containing audio bytes and metadata.
    """
    selected_model = model or DEFAULT_TTS_MODEL

    voice = request.voice if request.voice in OPENAI_TTS_VOICES else "alloy"

    client = get_sync_client()

    response = client.audio.speech.create(
        model=selected_model,
        voice=voice,
        input=request.text,
        speed=speed,
        response_format="mp3",
    )

    audio_bytes = response.content

    return SpokenBriefResponse(
        audio_bytes=audio_bytes,
        model_used=selected_model,
        voice_used=voice,
    )


def generate_spoken_brief_base64(
    request: SpokenBriefRequest,
    model: Optional[str] = None,
    speed: float = 1.0,
) -> SpokenBriefResponse:
    """
    Generate a spoken audio brief and return base64-encoded audio data.
    Uses OpenAI tts-1 model on api.openai.com.

    Args:
        request: SpokenBriefRequest with text and voice parameters.
        model: Optional explicit OpenAI TTS model identifier.
        speed: Speech speed multiplier.

    Returns:
        SpokenBriefResponse with base64-encoded audio_url field and metadata.
    """
    selected_model = model or DEFAULT_TTS_MODEL
    voice = request.voice if request.voice in OPENAI_TTS_VOICES else "alloy"

    client = get_sync_client()

    response = client.audio.speech.create(
        model=selected_model,
        voice=voice,
        input=request.text,
        speed=speed,
        response_format="mp3",
    )

    audio_bytes = response.content
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    audio_url = f"data:audio/mp3;base64,{audio_b64}"

    return SpokenBriefResponse(
        audio_bytes=audio_bytes,
        audio_url=audio_url,
        model_used=selected_model,
        voice_used=voice,
    )


if __name__ == "__main__":
    sample = SpokenBriefRequest(
        text="This is a spoken brief generated using OpenAI TTS.",
        voice="alloy",
        target_length_seconds=10,
    )
    result = generate_spoken_brief(sample)
    print(f"Model: {result.model_used}")
    print(f"Voice: {result.voice_used}")
    print(f"Audio size: {len(result.audio_bytes)} bytes")
