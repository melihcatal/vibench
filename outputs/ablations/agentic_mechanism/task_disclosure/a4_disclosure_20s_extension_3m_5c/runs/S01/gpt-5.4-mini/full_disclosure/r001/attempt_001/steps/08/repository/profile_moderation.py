import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]


def _api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def moderate_profile_text(text: str, model: str = "omni-moderation-latest") -> ModerationResult:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
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


def is_profile_approved(text: str, model: str = "omni-moderation-latest") -> bool:
    return not moderate_profile_text(text, model=model).flagged
