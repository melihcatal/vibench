from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass
class SafetyResult:
    unsafe: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    flagged_text: str
    raw: Dict[str, Any]


def _join_input(text: str, labels: Optional[Dict[str, str]] = None, annotations: Optional[List[str]] = None) -> str:
    parts = [text.strip()]
    if labels:
        parts.append("labels: " + json.dumps(labels, ensure_ascii=False, sort_keys=True))
    if annotations:
        parts.append("annotations: " + json.dumps(annotations, ensure_ascii=False))
    return "\n".join(part for part in parts if part)


def check_metric_annotation_safety(
    text: str,
    labels: Optional[Dict[str, str]] = None,
    annotations: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    timeout: float = 30.0,
) -> SafetyResult:
    payload_text = _join_input(text, labels=labels, annotations=annotations)
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": payload_text},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories = dict(result.get("categories", {}))
    category_scores = dict(result.get("category_scores", {}))
    unsafe = bool(result.get("flagged", False))
    return SafetyResult(
        unsafe=unsafe,
        categories=categories,
        category_scores=category_scores,
        flagged_text=payload_text,
        raw=data,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Check metric annotation safety with OpenAI Moderation.")
    parser.add_argument("text")
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--annotation", action="append", default=[])
    parser.add_argument("--api-key")
    args = parser.parse_args()

    labels = {}
    for item in args.label:
        if "=" in item:
            k, v = item.split("=", 1)
            labels[k] = v

    result = check_metric_annotation_safety(
        args.text,
        labels=labels or None,
        annotations=args.annotation or None,
        api_key=args.api_key,
    )
    print(json.dumps({
        "unsafe": result.unsafe,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
