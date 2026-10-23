from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI


def create_summary_client(api_key: str | None = None) -> OpenAI:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=key)


def summarize_meeting_chunks(chunks: Iterable[str]) -> str:
    client = create_summary_client()
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize a live meeting transcript into concise notes with action items.",
            },
            {
                "role": "user",
                "content": transcript,
            },
        ],
    )
    return response.output_text.strip()
