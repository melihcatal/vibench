import os
from typing import Any, Dict, Iterable

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


DEFAULT_THRESHOLDS = {
    "hate": 0.5,
    "hate/threatening": 0.2,
    "harassment": 0.6,
    "harassment/threatening": 0.2,
    "self-harm": 0.2,
    "self-harm/instructions": 0.1,
    "self-harm/intent": 0.1,
    "sexual": 0.7,
    "sexual/minors": 0.0,
    "violence": 0.6,
    "violence/graphic": 0.3,
}


def _get_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def moderate_text(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["results"][0]


def apply_category_thresholds(
    category_scores: Dict[str, float], thresholds: Dict[str, float] = DEFAULT_THRESHOLDS
) -> Dict[str, Any]:
    exceeded = {
        category: {"score": score, "threshold": threshold}
        for category, score in category_scores.items()
        if (threshold := thresholds.get(category)) is not None and score >= threshold
    }
    return {"allow": not exceeded, "blocked_categories": exceeded}


def allow_text(text: str, thresholds: Dict[str, float] = DEFAULT_THRESHOLDS) -> Dict[str, Any]:
    result = moderate_text(text)
    category_scores = result.get("category_scores", {})
    decision = apply_category_thresholds(category_scores, thresholds)
    return {
        "allow": decision["allow"],
        "blocked_categories": decision["blocked_categories"],
        "flagged": bool(result.get("flagged", False)),
        "raw": result,
    }


def _format_blocked(blocked_categories: Dict[str, Dict[str, float]]) -> str:
    return ", ".join(
        f"{name}={meta['score']:.3f}>={meta['threshold']:.3f}"
        for name, meta in blocked_categories.items()
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: safety_threshold.py TEXT")
    verdict = allow_text(sys.argv[1])
    print(verdict)
