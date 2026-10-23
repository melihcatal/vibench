from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def summarize_transcription_results(
    segments: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    text = "\n".join(
        segment.get("text", "") for segment in segments if segment.get("text")
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Create a concise archival summary of a completed speech-to-text transcript.",
            },
            {"role": "user", "content": text},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
    }
