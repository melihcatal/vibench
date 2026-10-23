from __future__ import annotations

import base64
from typing import Iterable

from openai import OpenAI

from embeddings_client import get_openai_client


AUDIO_MODEL = "gpt-4o-audio-preview"
AUDIO_VOICE = "alloy"


def retrieval_audio_brief(search_results: Iterable[str], model: str = AUDIO_MODEL, voice: str = AUDIO_VOICE) -> bytes:
    results = [result.strip() for result in search_results if result and result.strip()]
    if not results:
        raise ValueError("At least one retrieved search result is required.")

    client: OpenAI = get_openai_client()
    response = client.responses.create(
        model=model,
        modalities=["text", "audio"],
        audio={"voice": voice, "format": "wav"},
        input=(
            "Create a short spoken retrieval brief using these search findings: "
            + " | ".join(results[:5])
        ),
    )
    audio_b64 = response.output[0].content[0].audio.data
    return base64.b64decode(audio_b64)
