from __future__ import annotations

from typing import Iterable

from safety_client import OPENAI_SUMMARY_MODEL, get_openai_client
from safety_models import ModerationDecision


def summarize_moderation(decisions: Iterable[ModerationDecision]) -> str:
    packed = [
        {
            "allowed": item.allowed,
            "flagged": item.flagged,
            "action": item.action,
            "categories": [{"category": c.category, "score": c.score, "severity": c.severity} for c in item.categories],
        }
        for item in decisions
    ]
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize content moderation outcomes for policy analysts in concise plain English.",
            },
            {
                "role": "user",
                "content": f"Summarize these moderation decisions and highlight recurring risk categories: {packed}",
            },
        ],
    )
    return response.output_text
