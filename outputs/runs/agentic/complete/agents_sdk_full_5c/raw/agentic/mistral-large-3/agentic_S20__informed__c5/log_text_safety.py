from typing import List, Dict
import os
import requests


def check_log_text_safety(texts: List[str]) -> List[Dict[str, str]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []

    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"],
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            results.append({
                "text": text,
                "toxic": "true" if toxicity_score > 0.7 else "false",
                "score": str(toxicity_score),
            })
        else:
            results.append({
                "text": text,
                "toxic": "unknown",
                "score": "0.0",
            })
    return results