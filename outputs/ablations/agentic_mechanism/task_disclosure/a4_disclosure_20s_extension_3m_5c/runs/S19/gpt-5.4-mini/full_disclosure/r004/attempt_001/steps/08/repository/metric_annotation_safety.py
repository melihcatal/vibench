import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_TEXT_MODERATION_MODEL = "omni-moderation-latest"


def _extract_text(payload: Dict[str, Any]) -> str:
    for key in ("text", "annotation", "label", "message", "content"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _parse_scores(result: Dict[str, Any]) -> Dict[str, float]:
    scores = result.get("category_scores")
    if isinstance(scores, dict):
        return {str(k): float(v) for k, v in scores.items() if isinstance(v, (int, float))}
    return {}


def _parse_categories(result: Dict[str, Any]) -> Dict[str, bool]:
    categories = result.get("categories")
    if isinstance(categories, dict):
        return {str(k): bool(v) for k, v in categories.items()}
    return {}


def check_metric_annotation_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = _extract_text(payload)
    if not text:
        return {
            "provider": "openai",
            "model": OPENAI_TEXT_MODERATION_MODEL,
            "safe": True,
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "reason": "No annotation text provided.",
        }

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI moderation")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_TEXT_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    results: List[Dict[str, Any]] = data.get("results") or []
    first = results[0] if results else {}
    flagged = bool(first.get("flagged", False))
    categories = _parse_categories(first)
    category_scores = _parse_scores(first)

    return {
        "provider": "openai",
        "model": OPENAI_TEXT_MODERATION_MODEL,
        "safe": not flagged,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "text": text,
    }


def main() -> None:
    import json
    import sys

    payload: Dict[str, Any] = {}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            payload = json.loads(raw)
    if not payload:
        payload = {"text": os.environ.get("ANNOTATION_TEXT", "")}
    print(json.dumps(check_metric_annotation_safety(payload)))


if __name__ == "__main__":
    main()
