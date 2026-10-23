from typing import Dict, List
import os
import requests


class MetricAnnotationSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_unsafe_text(self, text: str) -> Dict:
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
        if response.status_code != 200:
            raise Exception(f"Perspective API request failed: {response.status_code}")

        result = response.json()
        return {
            "text": text,
            "toxicity": result.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0),
            "severe_toxicity": result.get("attributeScores", {})
            .get("SEVERE_TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0),
            "identity_attack": result.get("attributeScores", {})
            .get("IDENTITY_ATTACK", {})
            .get("summaryScore", {})
            .get("value", 0),
            "insult": result.get("attributeScores", {})
            .get("INSULT", {})
            .get("summaryScore", {})
            .get("value", 0),
            "profanity": result.get("attributeScores", {})
            .get("PROFANITY", {})
            .get("summaryScore", {})
            .get("value", 0),
            "threat": result.get("attributeScores", {})
            .get("THREAT", {})
            .get("summaryScore", {})
            .get("value", 0),
        }
