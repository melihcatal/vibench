import os
from typing import Dict

# Azure AI Content Safety client example
# Requires environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
class SafetyClient:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
        self.key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
        if not self.endpoint or not self.key:
            raise RuntimeError('Azure Content Safety endpoint and key must be set in environment variables')
        self.thresholds = {
            'hate': 0.5,
            'self_harm': 0.5,
            'sexual': 0.5,
            'violence': 0.5,
            # add more categories with custom thresholds if desired
        }

    def analyze_content(self, text: str) -> Dict[str, float]:
        # Placeholder for actual HTTP request to Azure API
        # Here we simulate a response format: {'categories': {'hate': 0.3, 'self_harm': 0.1, ...}}
        # In real code, you would use `requests.post(...)` with self.endpoint and self.key
        simulated_response = {
            'categories': {
                'hate': 0.2,
                'self_harm': 0.05,
                'sexual': 0.01,
                'violence': 0.4,
                # other categories omitted for brevity
            }
        }
        return simulated_response

    def batch_analyze(self, texts: list[str]) -> list[Dict[str, float]]:
        # Simulate batch processing by reusing analyze_content per text
        return [self.analyze_content(t) for t in texts]