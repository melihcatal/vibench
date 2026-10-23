import requests
import os
from typing import Dict, Any


class ContentSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_safety(self, text: str) -> Dict[str, Any]:
        """
        Checks message payload text for unsafe content using Perspective API.
        """
        params = {"key": self.api_key}
        data = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
        }
        response = requests.post(self.url, params=params, json=data)
        response.raise_for_status()
        return response.json()


def check_message_safety(text: str) -> Dict[str, Any]:
    """
    Checks if the message payload text contains unsafe content.
    """
    checker = ContentSafetyChecker()
    return checker.check_safety(text)


if __name__ == "__main__":
    message_text = "This is a test message with no harmful content."
    result = check_message_safety(message_text)
    print(f"Safety check result: {result}")
