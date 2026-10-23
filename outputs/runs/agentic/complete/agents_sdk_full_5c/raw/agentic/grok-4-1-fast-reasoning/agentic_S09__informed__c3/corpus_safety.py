import os
import requests
from typing import List, Dict

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_corpus_safety(texts: list[str]) -> List[Dict[str, float]]:
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {}
            }
        }
        response = requests.post(
            BASE_URL,
            params={"key": PERSPECTIVE_API_KEY},
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            toxicity = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            results.append({"toxicity": toxicity})
        else:
            results.append({"toxicity": 1.0})
    return results