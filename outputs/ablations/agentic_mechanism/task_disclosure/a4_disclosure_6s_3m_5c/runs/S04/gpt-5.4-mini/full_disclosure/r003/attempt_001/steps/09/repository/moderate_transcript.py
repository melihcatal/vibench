from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]


def _auth_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def moderate_transcript(text: str, model: str = OPENAI_MODERATION_MODEL) -> ModerationResult:
    payload = {"model": model, "input": text}
    response = requests.post(
        f"{OPENAI_API_BASE}/moderations",
        headers=_auth_headers(),
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return ModerationResult(
        flagged=bool(result.get("flagged", False)),
        categories=dict(result.get("categories", {})),
        category_scores=dict(result.get("category_scores", {})),
        raw=data,
    )


def moderate_transcript_segments(segments: List[Dict[str, Any]], model: str = OPENAI_MODERATION_MODEL) -> List[ModerationResult]:
    return [moderate_transcript(str(segment.get("text", "")), model=model) for segment in segments]
