import os
import requests

def profile_moderation(text: str) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    endpoint = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {}
        },
        "languages": ["en"]
    }
    response = requests.post(f"{endpoint}?key={api_key}", json=payload)
    response.raise_for_status()
    return response.json()