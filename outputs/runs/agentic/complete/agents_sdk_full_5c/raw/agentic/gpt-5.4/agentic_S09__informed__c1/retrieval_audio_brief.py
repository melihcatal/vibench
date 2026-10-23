from __future__ import annotations

import os
from typing import Sequence

from elevenlabs.client import ElevenLabs


def generate_retrieval_audio_brief(
    query: str,
    retrieved_passages: Sequence[str],
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required for ElevenLabs TTS")
    client = ElevenLabs(api_key=api_key)
    brief = " ".join(
        [f"Search brief for query: {query}."]
        + [f"Result {index + 1}: {passage}" for index, passage in enumerate(retrieved_passages)]
    )
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        text=brief,
    )
    return b"".join(audio)
