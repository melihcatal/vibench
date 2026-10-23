import os
import requests
from typing import List

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
API_KEY = os.getenv("PERSPECTICE_API_KEY")


def check_corpus_safety(texts: List[str]) -> List[bool]:
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "languages": ["en"],
        }
        response = requests.post(f"{PERSPECTIVE_URL}?key={API_KEY}", json=payload)
        if response.status_code == 200:
            scores = response.json().get("attributeScores", {})
            is_safe = all(
                scores.get(attr, {}).get("summaryScore", {}).get("value", 1.0) < 0.5
                for attr in scores
            )
            results.append(is_safe)
        else:
            results.append(False)
    return results
