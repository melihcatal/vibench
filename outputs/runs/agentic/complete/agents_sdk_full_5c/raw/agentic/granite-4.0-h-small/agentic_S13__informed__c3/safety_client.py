import os
import json
from safety_client import SafetyClient
from safety_models import SafetyModels

class SafetyClient:
    """Local wrapper for Azure AI Content Safety.
    Provides helper methods for authentication and request/response normalization.
    """
    def __init__(self, endpoint: str = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'),
                 key: str = os.getenv('AZURE_CONTENT_SAFETY_KEY')):
        self.endpoint = endpoint
        self.key = key
        self.headers = {'api-key': self.key}

    def detect(self, text: str) -> dict:
        """Send a single text to Azure and return the raw JSON response.
        In production this would use `requests.post(self.endpoint, json=payload, headers=self.headers)`.
        """
        # Placeholder implementation
        return {
            "input": {"type": "text", "text": text},
            "result": "safe",
            "categories": [
                {"name": "hate", "score": 0.1},
                {"name": "self_harm", "score": 0.05}
            ],
            "flags": []
        }

if __name__ == "__main__":
    client = SafetyClient()
    print(client.detect("Hello world."))
