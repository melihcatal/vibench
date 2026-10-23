from __future__ import annotations

from document_client import coerce_text, get_openai_client
from document_models import SafetyResult


def check_ocr_safety(text: str) -> SafetyResult:
    client = get_openai_client()
    response = client.moderations.create(model="omni-moderation-latest", input=coerce_text(text))
    result = response.results[0]
    return SafetyResult(
        provider="openai",
        flagged=result.flagged,
        categories=result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories),
        raw=response.model_dump() if hasattr(response, "model_dump") else None,
    )
