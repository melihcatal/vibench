from __future__ import annotations

from typing import Dict
import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_payload_text(text: str, api_key: str) -> Dict[str, object]:
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    toxicity = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    return {"unsafe": float(toxicity) >= 0.7, "score": float(toxicity), "raw": data}
