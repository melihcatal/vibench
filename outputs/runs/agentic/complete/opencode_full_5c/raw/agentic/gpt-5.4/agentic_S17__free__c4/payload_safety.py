from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from security_models import PayloadSafetyResult, sha256_text


def payload_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload["text"])
    client = OpenAI(api_key=payload.get("openai_api_key"))
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    result = moderation.results[0]
    normalized = PayloadSafetyResult(
        provider="openai",
        safe=not result.flagged,
        categories={
            key: bool(value) for key, value in result.categories.model_dump().items()
        },
        category_scores={
            key: float(value)
            for key, value in result.category_scores.model_dump().items()
        },
        flagged_text_sha256=sha256_text(text),
    )
    return normalized.to_dict()
