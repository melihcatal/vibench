# [LATER-STEP] script_safety.py
# Check narration scripts for unsafe content using Perspective API

import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")

API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_safety(script: str, context: dict = None) -> dict:
    """Submit the script to Perspective API and return the moderation scores.

    Args:
        script (str): Narration text to evaluate.
        context (dict, optional): Additional request context (e.g., clientInfo).

    Returns:
        dict: JSON response containing attribute scores.
    """
    payload = {
        "comment": {"text": script},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
        },
    }
    if context:
        payload["context"] = context
    headers = {"Content-Type": "application/json", "key": PERSPECTIVE_API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


# Example usage
if __name__ == "__main__":
    text = "This is a test comment."
    scores = check_safety(text)
    print("Perspective moderation scores:", scores)
