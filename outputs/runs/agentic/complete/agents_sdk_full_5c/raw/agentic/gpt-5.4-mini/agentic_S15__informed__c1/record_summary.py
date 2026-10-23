from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_ID = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def record_summary(record: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize retrieved document records in one concise paragraph."},
            {"role": "user", "content": str(record)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
