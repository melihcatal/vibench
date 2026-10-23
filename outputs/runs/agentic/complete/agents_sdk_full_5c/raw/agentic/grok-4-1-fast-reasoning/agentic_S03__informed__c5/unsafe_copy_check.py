import os
import requests

def unsafe_copy_check(text: str) -> dict[str, float]:
    """
    Check localized copy for unsafe content using Perspective API.
    Returns scores for toxicity attributes (0.0 to 1.0).
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "IDENTITY_ATTACK": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "doNotStore": True,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {}
    for key, value in result.get("attributeScores", {}).items():
        scores[key.lower()] = value["summaryScore"]["value"]
    return scores
