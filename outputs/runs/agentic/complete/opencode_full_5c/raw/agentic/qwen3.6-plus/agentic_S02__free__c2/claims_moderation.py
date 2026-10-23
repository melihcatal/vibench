from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "text-moderation-latest"
OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"


@dataclass
class ModerationResult:
    flagged: bool = False
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)
    model: str = ""
    raw_response: dict[str, Any] = field(default_factory=dict)


def moderate_claims(
    claims_text: str,
    api_key: str | None = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> ModerationResult:
    if not api_key:
        api_key = os.getenv(OPENAI_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(f"Environment variable {OPENAI_API_KEY_ENV} is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "input": claims_text,
        "model": model,
    }

    resp = requests.post(
        OPENAI_MODERATION_API_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    result_entry = data.get("results", [{}])[0]

    return ModerationResult(
        flagged=result_entry.get("flagged", False),
        categories=result_entry.get("categories", {}),
        category_scores=result_entry.get("category_scores", {}),
        model=data.get("model", model),
        raw_response=data,
    )


def moderate_federated_profile_notes(
    notes: list[str],
    api_key: str | None = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> list[ModerationResult]:
    results = []
    for note in notes:
        result = moderate_claims(note, api_key=api_key, model=model)
        results.append(result)
    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        result = moderate_claims(" ".join(sys.argv[1:]))
        print(f"Flagged: {result.flagged}")
        print(f"Categories: {result.categories}")
    else:
        print("Usage: python claims_moderation.py <text to moderate>")
