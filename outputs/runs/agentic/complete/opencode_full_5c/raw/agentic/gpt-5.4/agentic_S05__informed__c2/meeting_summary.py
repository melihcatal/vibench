from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI


def summarize_meeting_transcript(chunks: Iterable[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize live meeting transcript chunks into a concise meeting summary with actions.",
            },
            {"role": "user", "content": transcript},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
