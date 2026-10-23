import os
import requests
from typing import List


def corpus_safety(corpus_texts: List[str]) -> List[float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    scores = []
    for text in corpus_texts:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            toxicity = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            scores.append(toxicity)
        except Exception:
            scores.append(1.0)  # Assume unsafe on error

    return scores
