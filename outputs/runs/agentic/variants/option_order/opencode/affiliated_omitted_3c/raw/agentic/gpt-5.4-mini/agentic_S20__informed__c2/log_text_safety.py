import os
from typing import Dict

import requests


def check_text_safety(text: str) -> Dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    body = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(url, params={"key": api_key}, json=body, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    score = (
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return {"unsafe": score >= 0.5, "score": score, "raw": data}
