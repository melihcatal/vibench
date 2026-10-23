import os
import json
from typing import Dict, Any
import requests

# Perspective API configuration (text safety moderation)
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
PERSPECTIVE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

if not PERSPECTIVE_API_KEY:
    raise RuntimeError('PERSPECTIVE_API_KEY environment variable not set')


def moderate_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    '''Run free-text claims through Perspective API and return a moderated version.'''
    payload = {
        'comment': {'text': claims.get('notes', '')},
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_HATE': {}
        }
    }
    headers = {
        'key': PERSPECTIVE_API_KEY,
        'content-type': 'application/json'
    }
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    analysis = resp.json()['attributeScores']
    moderated = claims.copy()
    moderated['toxicity_score'] = analysis.get('TOXICITY', {}).get('summaryScore', {}).get('value')
    moderated['severe_toxicity_score'] = analysis.get('SEVERE_TOXICITY', {}).get('summaryScore', {}).get('value')
    moderated['identity_hate_score'] = analysis.get('IDENTITY_HATE', {}).get('summaryScore', {}).get('value')
    # Example moderation rule: flag any claim with severe toxicity > 0.5
    moderated['needs_review'] = moderated['severe_toxicity_score'] > 0.5
    return moderated

if __name__ == '__main__':
    # Demo usage
    sample_claims = {
        'user_id': '12345',
        'email': 'user@example.com',
        'notes': 'This is a potentially harmful statement about a group.'
    }
    result = moderate_claims(sample_claims)
    print(json.dumps(result, indent=2))
