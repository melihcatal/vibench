# [HELPER] safety_client.py

import os

# Example using Azure AI Content Safety (REST) as the concrete provider
# You can switch to another provider by adjusting the import and client creation below.

API_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')
API_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')

class SafetyClient:
    """Local helper that abstracts the external provider and exposes a simple check_content API."""

    def __init__(self):
        self.headers = {
            'api-key': API_KEY,
            'Content-Type': 'application/json',
        }

    def check_content(self, text: str) -> dict:
        """Call the provider and return a uniform moderation result."""
        import requests
        payload = {'input': {'text': text}}
        resp = requests.post(API_ENDPOINT, json=payload, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()
        # Normalize to our internal structure (decision + detailed scores + thresholds)
        decision = data.get('decision', 'safe')
        detailed = data.get('details', {})
        return {
            'decision': decision,
            'detailed': detailed,
            'thresholds': {
                'hate': 0.5,
                'selfHarm': 0.5,
                'sexual': 0.5,
                'violence': 0.5,
            },
        }
