import os
import requests
from vision_models import TextSafetyResult

class PerspectiveAPITextSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.api_key}"

    def check_text_safety(self, text: str) -> TextSafetyResult:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {}
            },
            "languages": ["en"]
        }

        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        result = response.json()

        attribute_scores = result.get("attributeScores", {})
        unsafe_categories = []

        for category, details in attribute_scores.items():
            if details["summaryScore"]["value"] > 0.7:
                unsafe_categories.append(category)

        return TextSafetyResult(
            is_safe=len(unsafe_categories) == 0,
            unsafe_categories=unsafe_categories
        )

def check_visual_safety_text(text: str) -> TextSafetyResult:
    checker = PerspectiveAPITextSafetyChecker()
    return checker.check_text_safety(text)