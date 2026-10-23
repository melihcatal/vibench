import os
from typing import List
import requests


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """Check corpus text for harmful content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}}
        }
        response = requests.post(url, json=payload)
        results.append(response.json())
    
    return {"safety_results": results}