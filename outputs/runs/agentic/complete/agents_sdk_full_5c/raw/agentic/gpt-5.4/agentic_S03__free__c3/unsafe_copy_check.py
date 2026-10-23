from __future__ import annotations

import json

from translation_client import get_openai_client
from translation_models import SafetyCheckResult


def check_localized_copy_safety(text: str, locale: str) -> SafetyCheckResult:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Classify localized marketing copy for safety. Return strict JSON with keys is_safe, categories, explanation.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Locale: {locale}\nText: {text}",
                    }
                ],
            },
        ],
    )
    payload = json.loads(response.output_text)
    return SafetyCheckResult(
        is_safe=bool(payload.get("is_safe", False)),
        categories=[str(item) for item in payload.get("categories", [])],
        explanation=str(payload.get("explanation", "")),
        provider="openai",
        raw=response.model_dump(),
    )
