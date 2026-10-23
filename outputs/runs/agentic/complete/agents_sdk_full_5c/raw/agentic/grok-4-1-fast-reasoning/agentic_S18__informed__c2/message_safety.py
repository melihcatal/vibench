import requests
import os
import json

PERSPECTICE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_message_safety(text: str, threshold: float = 0.7) -> dict:
    """
    Checks message payload text for unsafe content using Perspective API.
    Returns scores for toxicity attributes.
    """
    url = f"{BASE_URL}?key={PERSPECTICE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "IDENTITY_ATTACK": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    scores = response.json().get("attributeScores", {})
    score_dict = {
        attr: scores[attr]["summaryScore"]["value"] for attr in scores
    }
    is_safe = all(score < threshold for score in score_dict.values())
    return {"scores": score_dict, "is_safe": is_safe, "threshold": threshold}
