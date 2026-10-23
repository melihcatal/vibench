import os
from typing import Dict, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def _score_to_category(score: float, threshold: float) -> bool:
    return score < threshold


def allow_text(
    text: str,
    thresholds: Mapping[str, float],
    api_key: Optional[str] = None,
) -> bool:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    if not results:
        return False

    scores: Dict[str, float] = results[0].get("category_scores", {})
    for category, threshold in thresholds.items():
        if not _score_to_category(float(scores.get(category, 0.0)), float(threshold)):
            return False
    return True
