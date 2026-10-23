import os
import requests
import json

def moderate_claims(text: str) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "IDENTITY_ATTACK": {}
        }
    }
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json()