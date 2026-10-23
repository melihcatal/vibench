from __future__ import annotations

import os

from openai import OpenAI


MODEL = os.environ.get("OPENAI_ROTATION_MODEL", "gpt-4.1-mini")


def rotation_summary(notes: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarize secret rotation status in one concise paragraph."},
            {"role": "user", "content": notes},
        ],
    )
    return result.choices[0].message.content or ""
