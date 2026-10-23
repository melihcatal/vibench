from __future__ import annotations

from typing import Any, Dict

from model_client import get_audio_deployment, get_azure_openai_client


def platform_brief_audio(
    text: str, voice: str = "alloy", audio_format: str = "mp3"
) -> Dict[str, Any]:
    client = get_azure_openai_client(api_version="2025-01-01-preview")
    model = get_audio_deployment()
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        format=audio_format,
    )
    audio_bytes = response.read()
    return {
        "provider": "azure_openai",
        "model": model,
        "voice": voice,
        "format": audio_format,
        "audio": audio_bytes,
    }
