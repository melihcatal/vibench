import os

import requests


def payload_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = (
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return {"provider": "perspective-api", "unsafe": score >= 0.5, "score": score}
