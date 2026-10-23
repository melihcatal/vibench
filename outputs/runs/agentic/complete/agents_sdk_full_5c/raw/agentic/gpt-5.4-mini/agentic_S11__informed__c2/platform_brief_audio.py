from __future__ import annotations

from openai import AzureOpenAI

from model_client import get_client
from model_models import normalize_text


def platform_brief_audio(text: str) -> bytes:
    client: AzureOpenAI = get_client()
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=normalize_text(text),
    )
    return speech.read()
