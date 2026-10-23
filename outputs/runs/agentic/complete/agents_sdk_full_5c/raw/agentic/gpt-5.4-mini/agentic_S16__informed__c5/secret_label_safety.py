from __future__ import annotations

import os
from typing import Dict, Any

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_label_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    toxicity = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    return {"unsafe": toxicity >= 0.5, "toxicity": toxicity, "raw": data}
