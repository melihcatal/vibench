import os
import requests
from typing import Dict, Any
from safety_client import DEFAULT_THRESHOLDS
from safety_models import normalize_safety_scores

def moderate_text(text: str) -> Dict[str, Any]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {}
        },
        'languages': ['en']
    }
    params = {'key': api_key}
    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()
    data = response.json()
    scores = {}
    for attr, score_data in data['attributeScores'].items():
        scores[attr] = score_data['summaryScore']['value']
    return normalize_safety_scores(scores, DEFAULT_THRESHOLDS)