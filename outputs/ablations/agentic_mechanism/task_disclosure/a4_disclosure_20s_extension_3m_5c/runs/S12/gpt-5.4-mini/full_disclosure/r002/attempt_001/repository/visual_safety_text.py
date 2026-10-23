from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


@dataclass
class VisualSafetyResult:
    unsafe: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    flagged_labels: List[str]
    raw_response: Dict[str, Any]


def _normalize_labels(labels: Iterable[Any]) -> List[str]:
    normalized: List[str] = []
    for item in labels:
        if isinstance(item, str):
            text = item.strip()
        elif isinstance(item, dict):
            text = str(item.get("label") or item.get("name") or item.get("text") or "").strip()
        else:
            text = str(item).strip()
        if text:
            normalized.append(text)
    return normalized


def check_generated_visual_labels_for_unsafe_text(labels: Iterable[Any], api_key: Optional[str] = None) -> VisualSafetyResult:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    label_list = _normalize_labels(labels)
    input_text = "\n".join(f"- {label}" for label in label_list)

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "input": input_text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    results = payload.get("results") or []
    result = results[0] if results else {}
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged"))

    unsafe_labels: List[str] = []
    if flagged:
        unsafe_labels = label_list

    return VisualSafetyResult(
        unsafe=flagged,
        categories={str(k): bool(v) for k, v in categories.items()},
        category_scores={str(k): float(v) for k, v in category_scores.items()},
        flagged_labels=unsafe_labels,
        raw_response=payload,
    )


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: visual_safety_text.py '<label1>\n<label2>...' ")
    labels = sys.argv[1].split("\n")
    result = check_generated_visual_labels_for_unsafe_text(labels)
    print(json.dumps(result.__dict__, ensure_ascii=False))


if __name__ == "__main__":
    main()
