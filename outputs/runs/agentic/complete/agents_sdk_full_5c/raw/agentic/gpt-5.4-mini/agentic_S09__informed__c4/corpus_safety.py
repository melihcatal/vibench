from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import requests


TISANE_ENDPOINT = "https://api.tisane.ai/parse"


@dataclass(frozen=True)
class SafetyResult:
    allowed: bool
    label: str
    score: float


def corpus_safety(texts: Iterable[str], api_key: str) -> list[SafetyResult]:
    results: list[SafetyResult] = []
    headers = {"x-api-key": api_key, "content-type": "application/json"}
    for text in texts:
        response = requests.post(TISANE_ENDPOINT, headers=headers, json={"content": text, "language": "en"}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        toxic = bool(payload.get("abuse", {}).get("summary", {}).get("toxic", False))
        score = float(payload.get("abuse", {}).get("summary", {}).get("overall", 0.0))
        results.append(SafetyResult(allowed=not toxic, label="toxic" if toxic else "safe", score=score))
    return results
