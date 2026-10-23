from __future__ import annotations

import os
from typing import Iterable

from elevenlabs import ElevenLabs



def generate_retrieval_audio_brief(
    query: str,
    retrieved_results: Iterable[dict[str, object]],
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    highlights = []
    for index, item in enumerate(retrieved_results, start=1):
        document = str(item.get("document", ""))
        score = item.get("score", "n/a")
        highlights.append(f"Result {index} with score {score}: {document}")
    narrative = f"Search brief for query: {query}. " + " ".join(highlights)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=narrative,
    )
    return b"".join(audio)
