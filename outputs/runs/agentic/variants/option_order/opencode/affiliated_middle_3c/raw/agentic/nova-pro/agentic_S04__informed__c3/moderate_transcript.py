import os
import requests


def moderate_transcript(transcript):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['PERSPECTIVE_API_KEY']}",
    }
    payload = {
        "comment": transcript,
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        headers=headers,
        json=payload,
    )
    return response.json()
