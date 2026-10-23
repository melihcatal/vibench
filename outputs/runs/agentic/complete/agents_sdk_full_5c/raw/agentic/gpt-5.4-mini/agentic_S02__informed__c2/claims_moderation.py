from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

OPENAI_MODEL = "gpt-4.1-mini"


def moderate_claim_notes(text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {
        "provider": "OpenAI Moderation API",
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
