import os
import requests
from typing import List, Dict, Any

def check_corpus_safety(texts: List[str]) -> List[bool]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY required")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    safe_flags = []
    for text in texts:
        data: Dict[str, Any] = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}}
        }
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            score = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["mean"]
            safe_flags.append(score < 0.5)
        else:
            safe_flags.append(False)
    return safe_flags
