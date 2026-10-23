from __future__ import annotations

from pathlib import Path

from model_client import DEFAULT_TTS_MODEL, get_openai_client


def generate_spoken_brief(text: str, output_path: str, voice: str = "alloy") -> str:
    client = get_openai_client()
    destination = Path(output_path)
    with client.audio.speech.with_streaming_response.create(
        model=DEFAULT_TTS_MODEL,
        voice=voice,
        input=text,
        format="mp3",
    ) as response:
        response.stream_to_file(destination)
    return str(destination)
