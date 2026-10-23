from __future__ import annotations

from typing import Dict

import requests

PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def vendor_text_safety(text: str) -> Dict[str, float]:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    params = {"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")}
    response = requests.post(PERSPECTIVE_HOST, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"toxic_score": float(score)}
