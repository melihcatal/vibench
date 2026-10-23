from __future__ import annotations

import base64
import os
from typing import Any

from openai import OpenAI


def generate_audio_brief(search_results: list[dict[str, Any]], model: str = "gpt-4o-audio-preview", voice: str = "alloy") -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")
    client = OpenAI(api_key=api_key)
    summary_text = "\n".join(
        f"Title: {item.get('title', 'Untitled')} | Score: {item.get('score', 0)} | Snippet: {item.get('snippet', '')}"
        for item in search_results
    )
    response = client.responses.create(
        model=model,
        modalities=["text", "audio"],
        audio={"voice": voice, "format": "mp3"},
        input=f"Create a concise spoken brief from these retrieval results:\n{summary_text}",
    )
    audio_b64 = response.output[0].content[0].audio.data
    return {
        "provider": "OpenAI",
        "model": model,
        "voice": voice,
        "transcript": response.output_text,
        "audio_base64": audio_b64,
        "audio_bytes": base64.b64decode(audio_b64),
    }
