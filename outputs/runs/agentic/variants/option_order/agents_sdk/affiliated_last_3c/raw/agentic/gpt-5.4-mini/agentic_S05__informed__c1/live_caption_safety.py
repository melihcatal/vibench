from __future__ import annotations

import os

import requests

from speech_models import ModerationResult


class LiveCaptionSafetyChecker:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["PERSPECTIVE_API_KEY"]
        self.url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check(self, text: str) -> ModerationResult:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }
        response = requests.post(self.url, params={"key": self.api_key}, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return ModerationResult(text=text, unsafe=score >= 0.7, score=score, provider="Perspective API", raw=data)
