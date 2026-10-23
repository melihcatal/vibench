from __future__ import annotations

import os

import requests

from speech_models import ContentSafetyVerdict


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
        self.url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check(self, text: str) -> ContentSafetyVerdict:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
            "doNotStore": True,
        }
        response = requests.post(self.url, params={"key": self.api_key}, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        scores = {
            name.lower(): attr["summaryScore"]["value"]
            for name, attr in data.get("attributeScores", {}).items()
            if "summaryScore" in attr
        }
        toxicity = max(scores.values()) if scores else 0.0
        return ContentSafetyVerdict(text=text, unsafe=toxicity >= 0.5, score=toxicity, categories=scores, raw=data)
