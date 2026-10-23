# LATER-STEP ocr_safety.py

import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
MODERATION_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class SafetyChecker:
    """Check extracted text for unsafe content using Perspective API."""

    def __init__(self, api_key: str):
        self.headers = {
            "content-type": "application/json",
            "x-api-key": api_key,
        }

    def is_safe(self, text: str) -> bool:
        """Return True if text passes moderation, False otherwise."""
        payload = {
            "comment": {"text": text, "type": "PLAIN_TEXT"},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }
        resp = requests.post(MODERATION_ENDPOINT, headers=self.headers, json=payload)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Moderation request failed: {resp.status_code} {resp.text}"
            )
        result = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]
        # Return True for safety margin >= 0.5 (adjust as needed)
        return result["value"] < 0.5


if __name__ == "__main__":
    # Example usage – replace with real API key and text
    checker = SafetyChecker(PERSPECTIVE_API_KEY)
    text = "This is a sample comment."
    print("Safe?", checker.is_safe(text))
