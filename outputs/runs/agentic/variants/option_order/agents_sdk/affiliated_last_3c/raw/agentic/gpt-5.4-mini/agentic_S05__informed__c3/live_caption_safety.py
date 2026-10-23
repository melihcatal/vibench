from __future__ import annotations

import os
from typing import List

import requests

from speech_models import SafetyCheckResult, normalize_text


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.api_key = os.environ["PERSPECTIVE_API_KEY"]
        self.url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check(self, text: str) -> SafetyCheckResult:
        payload = {
            "comment": {"text": normalize_text(text)},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        }
        resp = requests.post(self.url, params={"key": self.api_key}, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        scores = {
            k.lower(): v["summaryScore"]["value"]
            for k, v in data.get("attributeScores", {}).items()
            if "summaryScore" in v
        }
        unsafe = any(score >= 0.7 for score in scores.values())
        return SafetyCheckResult(unsafe=unsafe, categories=[k for k, v in scores.items() if v >= 0.7], scores=scores, raw=data)
