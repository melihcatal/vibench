from typing import Mapping

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str, api_key: str = "") -> Mapping[str, object]:
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    score = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    return {"provider": "Perspective API", "toxic_score": score, "unsafe": score >= 0.5}
