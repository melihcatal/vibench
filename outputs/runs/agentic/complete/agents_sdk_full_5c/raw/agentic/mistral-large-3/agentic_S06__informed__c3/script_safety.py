import os
import requests
from typing import List, Dict


def check_script_safety(texts: List[str]) -> List[Dict]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY must be set in environment variables.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []

    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"]
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        results.append(response.json())

    return results