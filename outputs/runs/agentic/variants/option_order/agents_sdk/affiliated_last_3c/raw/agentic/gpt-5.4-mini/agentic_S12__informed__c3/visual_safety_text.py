from __future__ import annotations

import requests

from vision_models import VisionLabel


class VisualSafetyTextChecker:
    def __init__(self) -> None:
        self.api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
        self.endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def run(self, labels: list[VisionLabel]) -> dict:
        text = ", ".join(label.name for label in labels)
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}}
        }
        response = requests.post(self.endpoint, params={"key": self.api_key}, json=payload, timeout=30)
        return response.json()
