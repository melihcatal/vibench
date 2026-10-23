import os
import requests
from typing import Dict, Any

def check_annotation_safety(text: str, threshold: float = 0.5) -> Dict[str, Any]:
    """Check free-text metric labels or annotations for unsafe text using Perspective API."""
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable is required.')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANE': {},
            'THREAT': {},
            'IDENTITY_ATTACK': {}
        },
        'languages': ['en', 'es', 'fr']
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    scores = response.json()['attributeScores']
    issues = {k: v['summaryScore']['value'] > threshold for k, v in scores.items()}
    return {'scores': scores, 'issues': issues}