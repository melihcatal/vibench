import os
import requests
from safety_client import SizeLimitedJSONEncoder

# Perspective API
API_KEY = os.getenv('PERSPECTIVE_API_KEY')
BASE_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def moderate_batch(messages: list[str], threshold: float = 0.5) -> list[bool]:
    """Moderates a batch of user messages using Perspective API and returns per-message safety decisions.

    Each entry in the returned list corresponds to the safety decision for the respective message.
    """
    payload = {
        "comment": {"text": ""},
        "requestedAttributes": {"SEVERITY": {}}
    }
    # Perspective API expects a list of comments for batch mode
    payload["comments"] = [{"text": msg} for msg in messages]
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    response = requests.post(BASE_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    results = []
    for entry in response.json().get('attributeScores', {}).get('SEVERITY', []):
        score = entry.get('summaryScore', {}).get('value')
        results.append(score is not None and score <= threshold)
    # If fewer scores than messages, assume safe for missing entries
    while len(results) < len(messages):
        results.append(True)
    return results
