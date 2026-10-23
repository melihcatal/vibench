import os
import requests
from typing import List, Dict, Any

def check_text_safety(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        scores = response.json()["attributeScores"]
        return {k: scores[k]["summaryScore"]["mean"] for k in scores}
    return {}

def corpus_safety(corpus_texts: List[str]) -> List[Dict[str, float]]:
    return [check_text_safety(text) for text in corpus_texts]