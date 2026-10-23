import os
import requests
from speech_models import SafetyCheckRequest, SafetyCheckResponse

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

class LiveCaptionSafetyChecker:
    def __init__(self):
        self.api_key = PERSPECTIVE_API_KEY

    def check_safety(self, request: SafetyCheckRequest) -> SafetyCheckResponse:
        params = {"key": self.api_key}
        data = {
            "comment": {"text": request.text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {}
            },
            "languages": ["en"]
        }

        response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
        response.raise_for_status()
        result = response.json()

        categories = {}
        for attr in data["requestedAttributes"].keys():
            score = result["attributeScores"][attr]["summaryScore"]["value"]
            categories[attr] = score

        is_unsafe = any(score > 0.7 for score in categories.values())
        return SafetyCheckResponse(is_unsafe=is_unsafe, categories=categories)