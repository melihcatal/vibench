import os

import requests


def metric_annotation_safety(text):
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    score = (
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return {"unsafe": score >= 0.5, "score": score, "raw": data}
