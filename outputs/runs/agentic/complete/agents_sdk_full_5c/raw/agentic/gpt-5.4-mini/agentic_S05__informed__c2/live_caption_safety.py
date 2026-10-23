from __future__ import annotations

import os
from typing import List

import requests

from speech_models import normalize_caption


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
        self.endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check(self, text: str) -> dict:
        payload = {
            "comment": {"text": normalize_caption(text)},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"],
        }
        response = requests.post(
            f"{self.endpoint}?key={self.api_key}",
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
