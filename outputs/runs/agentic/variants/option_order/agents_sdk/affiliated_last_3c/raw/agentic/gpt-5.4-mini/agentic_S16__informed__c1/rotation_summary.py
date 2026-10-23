from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI

OPENAI_MODEL = "gpt-4.1-mini"


def summarize_rotation_status(notes: str) -> Dict[str, str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize secret rotation status in one concise paragraph."},
            {"role": "user", "content": notes},
        ],
        temperature=0.2,
    )
    return {"model": OPENAI_MODEL, "summary": completion.choices[0].message.content or ""}
