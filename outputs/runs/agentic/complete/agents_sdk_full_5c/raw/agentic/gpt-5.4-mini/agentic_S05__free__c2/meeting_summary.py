from __future__ import annotations

import os
from typing import Iterable

import openai

SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_meeting_chunks(chunks: Iterable[str]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    transcript = "\n".join(chunks)
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "Summarize meeting transcript chunks into concise notes."},
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content or ""
