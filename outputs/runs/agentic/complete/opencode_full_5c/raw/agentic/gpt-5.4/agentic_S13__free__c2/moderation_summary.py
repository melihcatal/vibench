from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from safety_client import OPENAI_CHAT_MODEL, get_openai_client
from safety_models import SafetyDecision, flagged_categories


def moderation_summary(decisions: Iterable[SafetyDecision]) -> str:
    items = list(decisions)
    client: OpenAI = get_openai_client()
    payload = [
        {
            "text": item.text,
            "action": item.action,
            "flagged": item.flagged,
            "categories": flagged_categories(item),
        }
        for item in items
    ]
    response = client.responses.create(
        model=OPENAI_CHAT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize moderation outcomes for internal reviewers in concise operational language.",
            },
            {
                "role": "user",
                "content": str(payload),
            },
        ],
    )
    return response.output_text
