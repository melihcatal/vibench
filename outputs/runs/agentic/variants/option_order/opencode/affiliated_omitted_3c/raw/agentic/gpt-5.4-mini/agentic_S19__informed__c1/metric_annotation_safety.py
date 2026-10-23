import os
import requests


def metric_annotation_safety(text, language="en"):
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "languages": [language], "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    return {"unsafe": score >= 0.5, "score": score, "provider": "Perspective API"}
