from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]


def moderate_claims(note: str, api_key: Optional[str] = None) -> ModerationResult:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": note},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    result = (payload.get("results") or [{}])[0]
    return ModerationResult(
        flagged=bool(result.get("flagged", False)),
        categories=dict(result.get("categories") or {}),
        category_scores=dict(result.get("category_scores") or {}),
        raw=payload,
    )


def moderate_claims_batch(notes: List[str], api_key: Optional[str] = None) -> List[ModerationResult]:
    return [moderate_claims(note, api_key=api_key) for note in notes]
