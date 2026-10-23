import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")

BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_live_caption_safety(text: str) -> dict:
    params = {"key": PERSPECTIVE_API_KEY}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "doNotStore": True
    }
    response = requests.post(BASE_URL, params=params, json=data)
    response.raise_for_status()
    scores = response.json().get("attributeScores", {})
    return scores

# Example usage:
# scores = check_live_caption_safety(caption_chunk)
# toxicity = scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)
# if toxicity > 0.5: print("Unsafe content detected")
