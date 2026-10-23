from __future__ import annotations

from typing import Any, Dict

import os
import requests

from observability_models import SafetyResult

TISANE_ENDPOINT = "https://api.tisane.ai"


def metric_annotation_safety(text: str, language: str = "en") -> SafetyResult:
    api_key = os.environ["TISANE_API_KEY"]
    response = requests.post(
        f"{TISANE_ENDPOINT}/parse",
        headers={"X-Tisane-Api-Key": api_key, "Content-Type": "application/json"},
        json={"content": text, "language": language},
        timeout=30,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    score = float(data.get("toxicity", 0.0))
    return SafetyResult(unsafe=score >= 0.5, score=score, categories={str(k): float(v) for k, v in dict(data.get("categories", {})).items()}, raw=data)
ta)
