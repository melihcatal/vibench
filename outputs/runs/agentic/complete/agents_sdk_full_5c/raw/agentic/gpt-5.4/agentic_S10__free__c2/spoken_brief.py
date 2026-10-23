from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from model_client import DEFAULT_AUDIO_MODEL, get_openai_client


def generate_spoken_brief(text: str, output_path: str, voice: str = "alloy") -> str:
    client: OpenAI = get_openai_client()
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with client.audio.speech.with_streaming_response.create(
        model=DEFAULT_AUDIO_MODEL,
        voice=voice,
        input=text,
        format="mp3",
    ) as response:
        response.stream_to_file(destination)
    return str(destination)
