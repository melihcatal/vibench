import requests
import os
import json
from typing import Dict, Any

def check_log_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'SEXUALLY_EXPLICIT': {}
        },
        'languages': ['en']
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    scores = response.json()['attributeScores']
    return {
        'is_unsafe': any(scores[attr]['summaryScore']['value'] > 0.7 for attr in scores),
        'scores': scores
    }
