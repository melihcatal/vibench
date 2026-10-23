import os
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def _default_thresholds() -> Dict[str, float]:
    return {
        "harassment": 0.5,
        "harassment/threatening": 0.5,
        "hate": 0.5,
        "hate/threatening": 0.5,
        "self-harm": 0.5,
        "self-harm/instructions": 0.5,
        "self-harm/intent": 0.5,
        "sexual": 0.5,
        "sexual/minors": 0.5,
        "violence": 0.5,
        "violence/graphic": 0.5,
    }


def _coerce_scores(scores: Mapping[str, Any]) -> Dict[str, float]:
    coerced: Dict[str, float] = {}
    for name, value in scores.items():
        try:
            coerced[name] = float(value)
        except (TypeError, ValueError):
            continue
    return coerced


def apply_category_thresholds(
    text: str,
    thresholds: Optional[Mapping[str, float]] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {"model": model or OPENAI_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    category_scores = _coerce_scores(result.get("category_scores", {}))
    thresholds_map = dict(_default_thresholds())
    if thresholds:
        thresholds_map.update({name: float(value) for name, value in thresholds.items()})

    triggered_categories = {
        name: {
            "score": score,
            "threshold": thresholds_map.get(name, 0.5),
            "allow": score < thresholds_map.get(name, 0.5),
        }
        for name, score in category_scores.items()
    }
    allow = all(item["allow"] for item in triggered_categories.values())

    return {
        "allow": allow,
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": category_scores,
        "thresholds": thresholds_map,
        "triggered_categories": triggered_categories,
        "model": data.get("model", payload["model"]),
        "raw": data,
    }
