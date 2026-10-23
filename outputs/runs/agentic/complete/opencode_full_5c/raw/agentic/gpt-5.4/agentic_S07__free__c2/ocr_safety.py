from __future__ import annotations

from document_client import get_default_safety_model, get_openai_client


def check_ocr_safety(text: str) -> dict:
    client = get_openai_client()
    response = client.moderations.create(
        model=get_default_safety_model(),
        input=text,
    )
    result = response.results[0]
    return {
        "provider": "openai",
        "model": get_default_safety_model(),
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories),
        "category_scores": result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores),
    }
