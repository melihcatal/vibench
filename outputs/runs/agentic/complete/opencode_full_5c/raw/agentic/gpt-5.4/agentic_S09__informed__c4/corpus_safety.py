from __future__ import annotations

import os
from typing import Any

import requests


def corpus_safety(texts: list[str], threshold: float = 0.7) -> dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results = []
    for text in texts:
        response = requests.post(
            url,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {"TOXICITY": {}},
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        score = payload["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        results.append({"text": text, "toxicity": score, "allowed": score < threshold})
    return {"provider": "Perspective API", "results": results}
