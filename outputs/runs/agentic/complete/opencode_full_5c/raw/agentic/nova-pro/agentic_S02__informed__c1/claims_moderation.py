import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def claims_moderation(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json", "API-Key": PERSPECTIVE_API_KEY}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload, headers=headers)
    analysis = response.json()
    return analysis["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.5
