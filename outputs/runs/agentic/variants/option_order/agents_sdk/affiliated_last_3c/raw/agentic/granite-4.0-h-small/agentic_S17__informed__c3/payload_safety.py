# [LATER-STEP] payload_safety.py

import os
import re
from typing import List

# Concrete Perspective API client using the HTTP REST interface.
class PerspectiveModeration:
    """Wrapper around the Perspective API for toxicity / unsafe content detection."""
    PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable.")

    def check_toxicity(self, text: str) -> List[dict]:
        """Send a request to Perspective API and return a list of attribute scores."""
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "IDENTITY_HATE": {}}
        }
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        import requests
        response = requests.post(self.PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["attributeScores"]

    def is_unsafe(self, text: str, unsafe_attribute: str = "SEVERE_TOXICITY") -> bool:
        """Return True if the text triggers the given unsafe attribute."""
        scores = self.check_toxicity(text)
        unsafe_score = scores.get(unsafe_attribute, {})
        # "summaryScore" contains the "value" field (0.0–1.0).
        return unsafe_score.get("summaryScore", {}).get("value", 0.0) >= 0.9


# Example helper function used by later-step processing pipelines.
def filter_unsafe_payloads(payloads: List[str]) -> List[str]:
    """Remove any payload that is considered unsafe by Perspective."""
    moderator = PerspectiveModeration()
    safe_payloads = [p for p in payloads if not moderator.is_unsafe(p)]
    return safe_payloads


if __name__ == "__main__":
    # Simple demo: run a few test strings through the moderator.
    test_strings = [
        "This is a harmless comment.",
        "You are an idiot and should be banned.",
        "I love ice cream."
    ]
    safe = filter_unsafe_payloads(test_strings)
    print("Safe payloads:", safe)
