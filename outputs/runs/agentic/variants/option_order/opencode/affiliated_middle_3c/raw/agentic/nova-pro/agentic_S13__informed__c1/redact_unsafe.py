import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def redact_unsafe(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}",
    }
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, headers=headers, json=data)
    toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"][
        "value"
    ]
    if toxicity_score > 0.5:
        return "[REDACTED]"
    return text
