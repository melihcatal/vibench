import os
import requests
import json

def vendor_text_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Set PERSPECTIVE_API_KEY")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {}
        },
        "doNotStore": True
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()

    result = resp.json()
    scores = {k: v["summaryScore"]["value"] for k, v in result["attributeScores"].items()}

    return {
        "safe": all(score < 0.5 for score in scores.values()),
        "scores": scores
    }