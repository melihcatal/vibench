from __future__ import annotations

from typing import Iterable

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def moderate_claims(notes: str, labels: Iterable[str] | None = None) -> dict[str, object]:
    client = OpenAI()
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=notes,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "labels": list(labels or []),
    }
