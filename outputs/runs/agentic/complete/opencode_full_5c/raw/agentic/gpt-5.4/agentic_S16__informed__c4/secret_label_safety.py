from __future__ import annotations

from typing import Any, Dict

import requests

from security_client import require_env


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def secret_label_safety(label: str, notes: str) -> Dict[str, Any]:
    api_key = require_env("PERSPECTIVE_API_KEY")
    text = "\n".join(part for part in (label, notes) if part)
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name: details["summaryScore"]["value"]
        for name, details in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "Perspective API",
        "scores": scores,
        "unsafe": any(value >= 0.7 for value in scores.values()),
    }
