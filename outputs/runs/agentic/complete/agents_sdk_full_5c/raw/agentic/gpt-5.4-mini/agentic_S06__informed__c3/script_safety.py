from __future__ import annotations

import os
from typing import Dict, Any

import requests


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def assess_script_safety(text: str) -> Dict[str, Any]:
    key = os.environ.get("PERSPECTIVE_API_KEY", "")
    if not key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(f"{PERSPECTIVE_API_HOST}?key={key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"toxicity": score, "raw": data}
