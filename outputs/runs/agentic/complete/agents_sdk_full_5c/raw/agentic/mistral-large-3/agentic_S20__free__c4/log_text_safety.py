from typing import List
import requests
import os

def check_log_text_safety(messages: List[str]) -> List[bool]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    results = []
    for message in messages:
        response = requests.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            params={"key": api_key},
            json={
                "comment": {"text": message},
                "requestedAttributes": {"TOXICITY": {}}
            }
        )
        results.append(response.json().get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0) < 0.5)
    return results