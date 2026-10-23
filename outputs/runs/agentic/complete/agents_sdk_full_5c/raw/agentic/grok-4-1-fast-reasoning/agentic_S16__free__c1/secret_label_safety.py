import requests
from typing import Dict, Any

from security_client import get_secrets_config

def check_secret_label_safety(text: str, threshold: float = 0.7) -> Dict[str, Any]:
    config = get_secrets_config()
    api_key = config['perspective_api_key']
    if not api_key:
        return {'error': 'PERSPECTIVE_API_KEY not set'}
    endpoint_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {}
        }
    }
    response = requests.post(endpoint_url, json=analyze_request)
    response.raise_for_status()
    result = response.json()
    toxicity_score = result['attributeScores']['TOXICITY']['summaryScore']['value']
    return {
        'toxicity_score': toxicity_score,
        'unsafe': toxicity_score > threshold
    }