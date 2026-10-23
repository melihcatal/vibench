import requests
import os
from typing import List, Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_log_safety(log_messages: List[str]) -> List[Dict[str, Any]]:
    results = []
    for message in log_messages:
        data = {
            "comment": {"text": message},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "PROFANITY": {},
            },
        }
        resp = requests.post(
            f"{PERSPECTIVE_URL}?key={PERSPECTIVE_API_KEY}", json=data
        ).json()
        scores = resp["attributeScores"]
        is_unsafe = scores["TOXICITY"]["summaryScore"]["value"] > 0.5
        results.append(
            {
                "message": message,
                "toxicity_score": scores["TOXICITY"]["summaryScore"]["value"],
                "is_unsafe": is_unsafe,
            }
        )
    return results
