from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI


def summarize_meeting_chunks(chunks: Iterable[str]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize a live meeting transcript into concise action-focused notes.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return response.output_text
