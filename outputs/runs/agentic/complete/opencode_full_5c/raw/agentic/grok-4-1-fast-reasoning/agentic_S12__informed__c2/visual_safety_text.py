import os
import requests
from typing import Dict, Any


def visual_safety_text(text_content: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    resp = requests.post(url, json=data)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]
    return {k: scores[k]["summaryScore"]["value"] for k in scores}
