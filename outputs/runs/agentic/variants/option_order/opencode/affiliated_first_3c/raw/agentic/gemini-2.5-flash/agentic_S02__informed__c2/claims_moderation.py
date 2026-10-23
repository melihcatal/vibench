import os
import requests
import json


def moderate_text_claim(text: str):
    PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
    if not PERSPECTIVE_API_KEY:
        raise ValueError("Missing PERSPECTIVE_API_KEY environment variable")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()
