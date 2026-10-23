import requests
from typing import List, Dict, Any

class UnsafeCopyChecker:
    def __init__(self):
        self.api_key = "YOUR_PERSPECTIVE_API_KEY"
        self.api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_unsafe_content(self, texts: List[str], language: str) -> List[Dict[str, Any]]:
        results = []
        for text in texts:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json={
                    "comment": {"text": text, "language": language},
                    "requestedAttributes": {
                        "TOXICITY": {},
                        "SEVERE_TOXICITY": {},
                        "IDENTITY_ATTACK": {}
                    }
                }
            )
            results.append(response.json())
        return results