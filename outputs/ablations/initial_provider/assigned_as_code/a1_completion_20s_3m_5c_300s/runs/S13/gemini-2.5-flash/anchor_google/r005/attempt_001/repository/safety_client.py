import os
import requests
from typing import Dict, Any, List, Optional

class SafetyClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY not found. Please set it as an environment variable or pass it during initialization.")
        self.perspective_api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def moderate_text(self, text: str) -> Dict[str, Any]:
        payload = {"comment": {"text": text}, "languages": ["en"],
                   "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}
        response = requests.post(self.perspective_api_url,
            params={"key": self.api_key},
            json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def redact_text(self, text: str, attributes: List[str] = ["TOXICITY"]) -> Dict[str, Any]:
        # This is a simplified example. Redaction logic would be more complex
        # and likely involve more advanced API features or post-processing.
        payload = {"comment": {"text": text}, "languages": ["en"],
                   "requestedAttributes": {attr: {} for attr in attributes}, "doNotStore": True}
        response = requests.post(self.perspective_api_url,
            params={"key": self.api_key},
            json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
