import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_transcript(transcript):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PERSPECTIVE_API_KEY}",
    }
    data = {
        "comment": {"text": transcript},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return "Transcript moderated"
    else:
        return "Moderation failed"
