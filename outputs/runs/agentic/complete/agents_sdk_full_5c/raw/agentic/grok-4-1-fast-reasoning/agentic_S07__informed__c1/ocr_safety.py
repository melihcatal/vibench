import os
import requests

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise ValueError("PERSPECTIVE_API_KEY not set")

def ocr_safety(text: str) -> dict:
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    scores = {
        attr: data["attributeScores"][attr]["summaryScore"]["value"]
        for attr in payload["requestedAttributes"]
    }
    return {
        "is_safe": min(scores.values()) < 0.5,
        "scores": scores,
    }