import requests
import os
from typing import Dict, Any, List


class TextSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_safety(self, text: str) -> Dict[str, Any]:
        params = {"key": self.api_key}
        data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
        response = requests.post(self.api_url, params=params, json=data)
        response.raise_for_status()
        return response.json()
