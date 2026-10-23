import os

import requests


def corpus_safety(text: str) -> bool:
    key = os.environ.get("PERSPECTIVE_API_KEY", "")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    return (
        response.ok
        and response.json()
        .get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
        < 0.5
    )
