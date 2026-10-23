from typing import Dict
from moderation_client import PerspectiveAPIClient


def profile_moderation(text: str) -> Dict[str, float]:
    client = PerspectiveAPIClient()
    response = client.analyze_text(text)
    return {
        "toxicity": response["attributeScores"]["TOXICITY"]["summaryScore"]["value"],
        "severe_toxicity": response["attributeScores"]["SEVERE_TOXICITY"][
            "summaryScore"
        ]["value"],
        "identity_attack": response["attributeScores"]["IDENTITY_ATTACK"][
            "summaryScore"
        ]["value"],
    }


class PerspectiveAPIClient:
    def __init__(self):
        self.api_key = "YOUR_PERSPECTIVE_API_KEY"
        self.url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.api_key}"

    def analyze_text(self, text: str) -> Dict:
        import requests

        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
            },
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()
