import os
import requests

# Perspective API
API_KEY = os.getenv('PERSPECTIVE_API_KEY')
BASE_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def moderate_text(text: str, threshold: float = 0.5) -> bool:
    """Scores user text for unsafe or policy-violating content using Perspective API.

    Returns True if the text is safe (score <= threshold), otherwise False.
    """
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"SEVERITY": {}}
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    response = requests.post(BASE_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    attr = response.json().get('attributeScores', {}).get('SEVERITY', {}).get('summaryScore')
    if not attr:
        raise RuntimeError('Unexpected response format')
    score = attr.get('value')
    return score <= threshold
