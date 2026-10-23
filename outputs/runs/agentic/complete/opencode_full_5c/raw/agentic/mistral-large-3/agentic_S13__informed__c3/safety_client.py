from typing import Dict, List, Optional, Union
import os
import requests


class PerspectiveClient:
    """Client for Google Perspective API to moderate text content."""

    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def moderate_text(
        self, text: str, requested_attributes: Optional[Dict[str, Dict]] = None
    ) -> Dict:
        """Moderate text using Perspective API and return raw response."""
        if requested_attributes is None:
            requested_attributes = {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            }

        payload = {
            "comment": {"text": text},
            "requestedAttributes": requested_attributes,
            "languages": ["en"],
        }

        params = {"key": self.api_key}
        response = requests.post(self.base_url, params=params, json=payload)
        response.raise_for_status()
        return response.json()
