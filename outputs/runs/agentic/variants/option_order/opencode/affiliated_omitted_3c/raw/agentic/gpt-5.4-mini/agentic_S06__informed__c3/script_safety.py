import os
from typing import Dict

import requests


def check_script_safety(text: str) -> Dict[str, float]:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": os.environ["PERSPECTIVE_API_KEY"]}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}}
    }
    resp = requests.post(url, params=params, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    scores = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
    return {"toxicity": scores.get("value", 0.0)}
