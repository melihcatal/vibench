import os
import requests


def moderate_transcript(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
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
        },
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    analysis = response.json()["attributeScores"]
    scores = {k: v["summaryScore"]["value"] for k, v in analysis.items()}
    is_flagged = any(score > 0.7 for score in scores.values())
    return {
        "flagged": is_flagged,
        "scores": scores,
        "safe": not is_flagged,
    }
