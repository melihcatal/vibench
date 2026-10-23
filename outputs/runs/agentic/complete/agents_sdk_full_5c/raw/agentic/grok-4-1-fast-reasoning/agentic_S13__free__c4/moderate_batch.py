import requests
from typing import List
from safety_client import PERSPECTIVE_API_KEY
from safety_models import SafetyResult

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="

ATTRIBUTES = {
    'TOXICITY': {},
    'SEVERE_TOXICITY': {},
    'IDENTITY_ATTACK': {},
    'INSULT': {},
    'PROFANITY': {},
    'THREAT': {},
    'SEXUALLY_EXPLICIT': {}
}

def moderate_batch(texts: List[str]) -> List[SafetyResult]:
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": ATTRIBUTES
        }
        response = requests.post(PERSPECTIVE_URL + PERSPECTIVE_API_KEY, json=payload).json()
        categories = {
            k: response["attributeScores"][k]["summaryScore"]["value"]
            for k in ATTRIBUTES
        }
        flagged = any(v > 0.5 for v in categories.values())
        severity = max(categories.values())
        results.append(SafetyResult(text, categories, flagged, severity))
    return results