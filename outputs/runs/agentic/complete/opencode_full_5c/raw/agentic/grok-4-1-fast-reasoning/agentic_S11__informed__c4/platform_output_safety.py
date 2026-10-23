import os
import requests
from typing import Dict, Any


def check_platform_output_for_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")
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
        },
        "doNotStore": True,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    analysis = response.json()
    scores = {
        attr: analysis["attributeScores"][attr]["summaryScore"]["value"]
        for attr in analysis["attributeScores"]
    }
    is_safe = all(score < 0.6 for score in scores.values())
    return {"is_safe": is_safe, "toxicity_scores": scores}
