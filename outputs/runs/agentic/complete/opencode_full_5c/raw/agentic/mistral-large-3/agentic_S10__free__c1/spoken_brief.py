from typing import Optional
import os
import httpx
from pydantic import BaseModel, Field


class TTSConfig(BaseModel):
    api_key: str = Field(..., description="API key for the text-to-speech service")
    base_url: str = Field(
        default="https://api.elevenlabs.io/v1/text-to-speech",
        description="Base URL for the ElevenLabs TTS API",
    )
    voice_id: str = Field(
        default="21m00Tcm4TlvDq8ikWAM",
        description="Voice identifier for TTS",
    )


def load_tts_config() -> TTSConfig:
    """Load TTS configuration from environment variables."""
    return TTSConfig(
        api_key=os.getenv("ELEVENLABS_API_KEY", ""),
        voice_id=os.getenv("TTS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
    )


async def generate_spoken_brief(text: str, voice_id: Optional[str] = None) -> bytes:
    """Generate a spoken brief from model output using ElevenLabs' hosted TTS API."""
    config = load_tts_config()
    voice_id = voice_id if voice_id else config.voice_id

    headers = {
        "xi-api-key": config.api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.base_url}/{voice_id}",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.content
