from __future__ import annotations

import os
import requests


def check_secret_label_safety(label: str, note: str) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    text = f"Label: {label}\nNote: {note}"
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in data.get("attributeScores", {}).items()
    }
    unsafe = any(score >= 0.7 for score in scores.values())
    return {
        "provider": "perspective-api",
        "endpoint": "commentanalyzer.googleapis.com",
        "text": text,
        "scores": scores,
        "unsafe": unsafe,
    }
