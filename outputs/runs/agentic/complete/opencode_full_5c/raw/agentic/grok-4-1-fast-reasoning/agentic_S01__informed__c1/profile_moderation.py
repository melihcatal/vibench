import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(profile_text: str) -> dict:
    payload = {
        "comment": {"text": profile_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(ENDPOINT + "?key=" + PERSPECTIVE_API_KEY, json=payload)
    response.raise_for_status()
    data = response.json()
    scores = data["attributeScores"]
    return {
        "is_safe": all(scores[attr]["summaryScore"]["value"] < 0.5 for attr in scores),
        "scores": {k: v["summaryScore"]["value"] for k, v in scores.items()},
    }
