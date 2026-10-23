from __future__ import annotations

from typing import Dict

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str, api_key: str | None = None) -> Dict[str, object]:
    params = {"key": api_key} if api_key else {}
    body = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=body, timeout=20)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return {"unsafe": any(v.get("summaryScore", {}).get("value", 0) >= 0.5 for v in scores.values()), "raw": data}
