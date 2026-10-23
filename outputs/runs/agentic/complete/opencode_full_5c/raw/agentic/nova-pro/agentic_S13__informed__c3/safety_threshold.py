import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def safety_threshold(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    headers = {"Content-Type": "application/json", "key": PERSPECTIVE_API_KEY}
    response = requests.post(url, json=payload, headers=headers)
    toxicity_score = (
        response.json()
        .get("attributeScores", {})
        .get("TOXICITY", [{}])[0]
        .get("summaryScore", {})
        .get("value", 0)
    )
    return toxicity_score <= 0.5
