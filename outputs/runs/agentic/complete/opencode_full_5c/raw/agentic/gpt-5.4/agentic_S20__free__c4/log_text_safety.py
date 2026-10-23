from __future__ import annotations

import os

from openai import OpenAI


def log_text_safety(message_text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=message_text,
    )
    result = response.results[0]
    if result.flagged:
        return "flagged"
    return "safe"
