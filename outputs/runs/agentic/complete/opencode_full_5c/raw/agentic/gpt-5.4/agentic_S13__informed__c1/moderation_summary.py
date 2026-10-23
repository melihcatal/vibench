from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from safety_models import ModerationDecision


def moderation_summary(decisions: Iterable[ModerationDecision]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    serialized: List[dict] = []
    for item in decisions:
        serialized.append(
            {
                "text": item.text,
                "flagged": item.flagged,
                "action": item.action,
                "categories": item.categories,
                "reasons": item.reasons,
            }
        )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize moderation outcomes for an internal trust and safety reviewer in concise operational language.",
            },
            {
                "role": "user",
                "content": str(serialized),
            },
        ],
    )
    return response.output_text
