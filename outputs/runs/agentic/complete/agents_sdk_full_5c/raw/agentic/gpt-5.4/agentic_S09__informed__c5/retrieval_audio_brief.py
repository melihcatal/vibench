from __future__ import annotations

import os
from collections.abc import Sequence

from elevenlabs.client import ElevenLabs


def generate_retrieval_audio_brief(
    results: Sequence[str],
    *,
    voice_id: str | None = None,
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    if not results:
        raise ValueError("at least one retrieval result is required")
    client = ElevenLabs(api_key=api_key)
    selected_voice = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
    brief_text = "Search brief: " + " ".join(item.strip() for item in results if item and item.strip())
    audio_stream = client.text_to_speech.convert(
        voice_id=selected_voice,
        model_id=model_id,
        text=brief_text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio_stream)
