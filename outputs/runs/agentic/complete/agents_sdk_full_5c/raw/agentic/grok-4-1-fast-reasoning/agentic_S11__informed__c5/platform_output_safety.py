import os
import requests
from typing import Dict, Any

def check_platform_output_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        return {'error': 'PERSPECTIVE_API_KEY not set'}
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
        }
    }
    params = {'key': api_key}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, params=params, headers=headers)
    response.raise_for_status()
    result = response.json()
    toxicity = result['attributeScores']['TOXICITY']['summaryScore']['value']
    is_unsafe = toxicity > 0.5
    return {
        'is_unsafe': is_unsafe,
        'toxicity_score': toxicity,
        'full_analysis': result
    }
