from __future__ import annotations

from typing import Any

from openai import OpenAI


OPENAI_MODEL = "omni-moderation-latest"


def record_text_safety(document: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    client = OpenAI()
    text_parts = []
    for field in fields:
        if field in document and document[field] is not None:
            text_parts.append(f"{field}: {document[field]}")
    moderation = client.moderations.create(
        model=OPENAI_MODEL, input="\n".join(text_parts)
    )
    result = moderation.results[0]
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories),
        "category_scores": result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores),
    }
