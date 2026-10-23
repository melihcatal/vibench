import os
import requests
from typing import List, Dict


def check_corpus_safety(corpus_texts: List[str]) -> List[Dict[str, float]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    attributes = [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "IDENTITY_ATTACK",
        "INSULT",
        "PROFANITY",
        "THREAT",
    ]
    results = []
    for text in corpus_texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in attributes},
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        scores = {
            attr: data["attributeScores"][attr]["summaryScore"]["value"]
            for attr in attributes
        }
        results.append(scores)
    return results
