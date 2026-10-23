import os
from typing import Optional
from model_client import get_llm_client


def generate_spoken_brief(
    text: str,
    voice: Optional[str] = "alloy",
    model: Optional[str] = "tts-1"
) -> bytes:
    """
    Generate a spoken brief from the model output using OpenAI's Text-to-Speech API.
    """
    client = get_llm_client()
    response = client.post(
        "https://api.openai.com/v1/audio/speech",
        json={
            "model": model,
            "input": text,
            "voice": voice
        },
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return response.content