from __future__ import annotations

import os
from typing import Dict

import requests

from speech_models import SafetyVerdict


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("PERSPECTIVE_API_KEY is required for Perspective API")
        self.endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check(self, text: str) -> SafetyVerdict:
        payload: Dict[str, object] = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}, "SEXUALLY_EXPLICIT": {}},
        }
        response = requests.post(self.endpoint, params={"key": self.api_key}, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        categories = {}
        unsafe = False
        for name, attr in data.get("attributeScores", {}).items():
            score = float(attr.get("summaryScore", {}).get("value", 0.0))
            categories[name] = score
            unsafe = unsafe or score >= 0.5
        return SafetyVerdict(text=text, unsafe=unsafe, categories=categories, raw={"provider": "perspective-api", "response": data})
