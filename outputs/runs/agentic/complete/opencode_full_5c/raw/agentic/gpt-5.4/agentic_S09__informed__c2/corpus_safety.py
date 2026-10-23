from __future__ import annotations

import os

import requests


def corpus_safety(text: str) -> dict[str, object]:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    return {
        "allowed": max(scores.values(), default=0.0) < 0.7,
        "scores": scores,
    }
