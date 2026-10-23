import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def claims_moderation(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PERSPECTIVE_API_KEY}",
    }
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
