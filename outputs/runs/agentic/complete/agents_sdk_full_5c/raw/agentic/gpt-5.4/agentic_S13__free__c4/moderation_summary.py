from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from safety_models import ModerationDecision


OPENAI_MODEL = "gpt-4o-mini"


def moderation_summary(decisions: Iterable[ModerationDecision]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    rendered = []
    for item in decisions:
        rendered.append(
            {
                "text": item.text,
                "allowed": item.allowed,
                "categories": [{"category": c.category, "score": c.score} for c in item.categories],
                "reason": item.reason,
            }
        )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Summarize moderation outcomes for a trust and safety reviewer."},
            {"role": "user", "content": str(rendered)},
        ],
    )
    return response.output_text
