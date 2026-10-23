import os
import json
from typing import Dict, Any

# Placeholder for content moderation of free-text claims
# Uses Azure AI Content Safety API for demonstration

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

import requests

def moderate_claim(claim_text: str) -> Dict[str, Any]:
    """Run text through Azure Content Safety and return moderation results."""
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/detect"
    headers = {
        'Content-Type': 'application/json',
        'api-key': AZURE_CONTENT_SAFETY_KEY
    }
    payload = {
        'input': {
            'text': claim_text
        },
        'properties': {
            # Example properties; adjust per API version
            'category': 'all',
            'severity': 'all'
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()
    # Normalize result to internal moderation schema
    moderation = {
        'original_text': claim_text,
        'safe': result.get('safe', False),
        'violations': result.get('violations', [])
    }
    return moderation

if __name__ == '__main__':
    # Example: moderate a claim entered by a federated user
    claim = os.getenv('CLAIM_TEXT', 'This is a test claim with no issues.')
    moderation = moderate_claim(claim)
    print(json.dumps(moderation, indent=2))
