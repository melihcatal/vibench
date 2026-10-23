from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY_ENV = "PERSPECTIVE_API_KEY"


@dataclass
class SafetyResult:
    unsafe: bool
    score: float
    categories: Dict[str, float]
    raw: Dict[str, Any]


def _build_payload(text: str) -> Dict[str, Any]:
    return {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "languages": ["en"],
        "doNotStore": True,
    }


def _extract_scores(response_json: Dict[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    attr_scores = response_json.get("attributeScores", {})
    for key, value in attr_scores.items():
        summary = value.get("summaryScore", {})
        score = summary.get("value")
        if isinstance(score, (int, float)):
            scores[key] = float(score)
    return scores


def check_metric_annotation_safety(text: str, threshold: float = 0.5, api_key: Optional[str] = None) -> SafetyResult:
    key = api_key or os.getenv(PERSPECTIVE_API_KEY_ENV)
    if not key:
        raise ValueError("Missing Perspective API key")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": key},
        headers={"Content-Type": "application/json"},
        data=json.dumps(_build_payload(text)),
        timeout=30,
    )
    response.raise_for_status()
    response_json = response.json()
    scores = _extract_scores(response_json)
    toxicity = max(scores.values()) if scores else 0.0
    return SafetyResult(
        unsafe=toxicity >= threshold,
        score=toxicity,
        categories=scores,
        raw=response_json,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()
    result = check_metric_annotation_safety(args.text, args.threshold)
    print(json.dumps({"unsafe": result.unsafe, "score": result.score, "categories": result.categories, "raw": result.raw}))


if __name__ == "__main__":
    main()
