import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def redact_unsafe(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"Content-Type": "application/json", "API_KEY": PERSPECTIVE_API_KEY}
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    if result["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.5:
        return "[REDACTED]"
    return text
