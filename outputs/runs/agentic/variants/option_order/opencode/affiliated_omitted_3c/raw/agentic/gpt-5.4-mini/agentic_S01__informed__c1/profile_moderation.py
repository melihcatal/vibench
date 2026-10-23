import os

import requests

from identity_models import normalize_profile_text


def profile_moderation(text: str):
    cleaned = normalize_profile_text(text)
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": cleaned},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
