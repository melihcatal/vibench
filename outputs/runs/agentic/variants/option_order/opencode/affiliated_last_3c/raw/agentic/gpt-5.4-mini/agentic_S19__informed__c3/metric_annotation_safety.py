import os

import requests


def metric_annotation_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not api_key:
        return {"safe": False, "reason": "missing_api_key"}
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    data = resp.json()
    score = (
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return {"safe": score < 0.5, "score": score}
