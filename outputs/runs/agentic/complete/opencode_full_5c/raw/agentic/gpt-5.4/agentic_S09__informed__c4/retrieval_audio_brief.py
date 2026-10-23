from __future__ import annotations

import os

from elevenlabs import ElevenLabs


def retrieval_audio_brief(
    results: list[dict[str, object]],
    voice_id: str,
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    lines = []
    for index, item in enumerate(results[:5], start=1):
        lines.append(f"Result {index}: {item.get('text', '')}")
    text = " ".join(lines)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
