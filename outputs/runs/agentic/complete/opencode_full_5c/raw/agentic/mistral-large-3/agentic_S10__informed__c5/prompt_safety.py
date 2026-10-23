import os
from typing import Dict, Any, Optional

import requests


class PromptSafetyClient:
    """Client for Perspective API to check prompts and generated text for unsafe content."""

    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_safety(self, text: str) -> Dict[str, Any]:
        """Check text for unsafe content using Perspective API."""
        params = {"key": self.api_key}
        request_body = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "languages": ["en"],
        }

        response = requests.post(self.base_url, params=params, json=request_body)
        response.raise_for_status()
        return response.json()


def check_prompt_safety(text: str) -> Dict[str, Any]:
    """Check if prompt or generated text contains unsafe content using Perspective API."""
    client = PromptSafetyClient()
    return client.check_safety(text)
