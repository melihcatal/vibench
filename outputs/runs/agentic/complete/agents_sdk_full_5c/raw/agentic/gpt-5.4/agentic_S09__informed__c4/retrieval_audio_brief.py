from __future__ import annotations

import os
from collections.abc import Sequence

from elevenlabs.client import ElevenLabs


ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"


def generate_retrieval_audio_brief(
    query: str,
    retrieved_results: Sequence[str],
    *,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = ELEVENLABS_MODEL_ID,
) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError("ELEVENLABS_API_KEY is required for ElevenLabs text-to-speech")

    client = ElevenLabs(api_key=api_key)
    brief = "Query: " + query.strip() + "\n\nTop retrieved findings:\n- " + "\n- ".join(
        item.strip() for item in retrieved_results if str(item).strip()
    )
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=brief,
        output_format="mp3_44100_128",
    )
    return b"".join(audio_stream)
