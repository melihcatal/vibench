import os
import requests


class PerspectiveAPIClient:
    """Check localized copy for unsafe content using Perspective API."""

    def __init__(self):
        self.api_key = os.getenv('PERSPECTIVE_API_KEY')
        self.base_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_unsafe_content(self, text: str) -> Dict[str, Any]:
        """Check text for unsafe content."""
        params = {"key": self.api_key}
        data = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {}
            }
        }
        
        response = requests.post(self.base_url, params=params, json=data)
        response.raise_for_status()
        return response.json()


def unsafe_copy_check(text: str) -> Dict[str, Any]:
    """Check localized copy for unsafe content using Perspective API."""
    client = PerspectiveAPIClient()
    return client.check_unsafe_content(text)