import os
import requests
from typing import List, Dict, Any


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """Checks corpus text before embedding using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = {}
    for i, text in enumerate(texts):
        if not text.strip():
            results[f"text_{i}"] = {"error": "Empty text provided."}
            continue

        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            results[f"text_{i}"] = response.json()
        except requests.exceptions.RequestException as e:
            results[f"text_{i}"] = {"error": str(e)}
    return results
