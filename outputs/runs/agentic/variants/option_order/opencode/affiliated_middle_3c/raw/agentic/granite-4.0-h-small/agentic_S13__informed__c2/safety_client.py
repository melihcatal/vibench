import os
import requests


class SafetyClient:
    """
    Lightweight wrapper around a hosted safety model service.
    Provides configuration loading and request/response handling.
    """

    # ----------------------------------------------------------------------
    # Configuration loading
    # ----------------------------------------------------------------------
    def __init__(self):
        # Load API key from environment (example: Perspective API)
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")

    # ----------------------------------------------------------------------
    # Request handling
    # ----------------------------------------------------------------------
    def moderate(self, user_text: str) -> dict:
        """Score user text for unsafe content using Perspective API."""
        endpoint = "https://commentanalyzer.googleapis.com/v1/analyze"
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {
            "comment": {"text": user_text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_HATE": {},
            },
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return {"text": user_text, "scores": result.get("attributeScores", {})}
