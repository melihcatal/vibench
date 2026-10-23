import requests
import os
import json


def profile_moderation(profile_text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": profile_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "IDENTITY_ATTACK": {},
        },
        "doNotStore": True,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()
