from typing import List, Dict
import os
import requests
from pydantic import BaseModel

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"


class AudioBriefRequest(BaseModel):
    text: str
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Default voice ID for Rachel
    model_id: str = "eleven_multilingual_v2"
    stability: float = 0.5
    similarity_boost: float = 0.5


def generate_spoken_brief(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    """Generate a spoken brief from text using ElevenLabs text-to-speech API."""
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set.")

    request = AudioBriefRequest(text=text, voice_id=voice_id)
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}

    response = requests.post(
        f"{ELEVENLABS_API_URL}/{voice_id}",
        json={
            "text": request.text,
            "model_id": request.model_id,
            "voice_settings": {
                "stability": request.stability,
                "similarity_boost": request.similarity_boost,
            },
        },
        headers=headers,
    )
    response.raise_for_status()

    return response.content


def retrieval_audio_brief(retrieved_results: List[Dict[str, str]]) -> bytes:
    """Generate a spoken brief from retrieved search results using ElevenLabs API."""
    brief_text = "Here are the top results:\n"
    for idx, result in enumerate(retrieved_results, 1):
        brief_text += f"Result {idx}: {result.get('content', '')}\n"

    return generate_spoken_brief(brief_text)
