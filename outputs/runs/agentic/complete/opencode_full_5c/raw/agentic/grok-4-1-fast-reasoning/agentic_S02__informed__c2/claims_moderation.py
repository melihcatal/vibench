import requests
import os
from identity_models import UserProfile

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_free_text_claims(text: str) -> dict:
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json().get("attributeScores", {})


def moderate_profile(profile: UserProfile) -> dict:
    text = profile.name or profile.email or ""
    return moderate_free_text_claims(text)
