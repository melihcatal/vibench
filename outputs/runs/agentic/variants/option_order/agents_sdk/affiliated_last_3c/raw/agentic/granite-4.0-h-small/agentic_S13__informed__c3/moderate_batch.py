import os
import requests
from typing import List, Dict

# Perspective API integration
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyzeScore"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def moderate_batch(messages: List[str], threshold: float = 0.5) -> List[Dict]:
    """Moderate a batch of user messages using Perspective API.

    Returns a list of dicts with the original text, TOXICITY score, and
    a flag indicating if the message exceeds the safety threshold.
    """
    payloads = [
        {
            "comment": {
                "text": msg,
                "type": "PLAIN_TEXT"
            },
            "requestedAttributes": {
                "TOXICITY": {}
            }
        }
        for msg in messages
    ]
    headers = {
        "content-type": "application/json",
        "x-goog-api-key": PERSPECTIVE_API_KEY
    }
    response = requests.post(API_URL, json={"messages": payloads}, headers=headers)
    response.raise_for_status()
    results = response.json()["results"]
    output = []
    for msg, result in zip(messages, results):
        score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        output.append({
            "text": msg,
            "toxicity_score": score,
            "exceeds_threshold": score >= threshold
        })
    return output
