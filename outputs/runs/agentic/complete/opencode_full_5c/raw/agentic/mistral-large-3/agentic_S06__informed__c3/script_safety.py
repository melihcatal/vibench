import os
import requests
from typing import Dict, List


class ScriptSafetyChecker:
    """Checks narration scripts for unsafe content using Perspective API."""

    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_safety(self, text: str, attributes: List[str] = None) -> Dict:
        """
        Checks the text for unsafe content.

        Args:
            text: The text to analyze.
            attributes: List of attributes to analyze (e.g., ["TOXICITY", "SEVERE_TOXICITY"]).

        Returns:
            Dict: The safety analysis results.

        Raises:
            Exception: If the request fails.
        """
        if attributes is None:
            attributes = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK"]

        payload = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in attributes},
            "languages": ["en"],
        }
        params = {"key": self.api_key}

        response = requests.post(self.api_url, params=params, json=payload)
        response.raise_for_status()
        return response.json()
