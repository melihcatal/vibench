from __future__ import annotations

import os

import requests

from speech_models import SafetyResult


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
        self.endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check(self, text: str) -> SafetyResult:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }
        params = {"key": self.api_key}
        response = requests.post(self.endpoint, params=params, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return SafetyResult(label="TOXICITY", score=float(score), raw=data)
