import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_safety(text: str) -> dict:
    """Submit text to Perspective API and receive toxicity scores.

    Returns a full JSON response containing `attributeScores`.
    """
    headers = {
        "X-Goog-Api-Key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


# Sample usage (kept commented out)
# result = check_safety('This is a sample comment')
# print(result)
