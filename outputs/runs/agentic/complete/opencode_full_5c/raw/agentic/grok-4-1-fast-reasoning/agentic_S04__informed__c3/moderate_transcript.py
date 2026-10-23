import os
import requests
from typing import List, Dict, Any


def moderate_transcript(segments: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set.")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    scores = []
    for text in segments:
        data = {
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
        response = requests.post(url, json=data)
        response.raise_for_status()
        scores.append(response.json())
    return scores
