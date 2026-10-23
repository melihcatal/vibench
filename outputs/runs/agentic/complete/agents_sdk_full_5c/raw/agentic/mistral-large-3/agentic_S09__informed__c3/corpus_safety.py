import os
import requests


class CorpusSafetyChecker:
    """Check corpus text for safety using Perspective API."""

    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
        self.base_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_text(self, text: str) -> Dict[str, Any]:
        params = {"key": self.api_key}
        payload = {
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
        response = requests.post(self.base_url, params=params, json=payload)
        response.raise_for_status()
        return response.json()

    def is_safe(self, text: str, threshold: float = 0.7) -> bool:
        result = self.check_text(text)
        attribute_scores = result.get("attributeScores", {})
        for attribute in attribute_scores:
            score = attribute_scores[attribute].get("summaryScore", {}).get("value", 0.0)
            if score > threshold:
                return False
        return True


def check_corpus_safety(text: str) -> bool:
    return CorpusSafetyChecker().is_safe(text)