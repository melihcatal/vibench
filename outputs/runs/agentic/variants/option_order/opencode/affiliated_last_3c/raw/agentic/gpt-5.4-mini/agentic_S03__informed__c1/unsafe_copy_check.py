import os
from typing import Dict

import requests


class UnsafeCopyChecker:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("PERSPECTIVE_API_KEY", "")
        self.endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check(self, text: str) -> Dict[str, float]:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
        }
        response = requests.post(self.endpoint, params={"key": self.api_key}, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        attrs = data.get("attributeScores", {})
        return {name.lower(): score.get("summaryScore", {}).get("value", 0.0) for name, score in attrs.items()}


def unsafe_copy_check(text: str) -> Dict[str, float]:
    return UnsafeCopyChecker().check(text)
