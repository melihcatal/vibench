from __future__ import annotations

import os

import requests


class LiveCaptionSafety:
    PERSPECTIVE_API_URL = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    )

    def __init__(self) -> None:
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise RuntimeError("PERSPECTIVE_API_KEY is required")

    def analyze_text(self, text: str) -> dict:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        }
        response = requests.post(
            self.PERSPECTIVE_API_URL,
            params={"key": self.api_key},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def is_unsafe(self, text: str, threshold: float = 0.8) -> bool:
        data = self.analyze_text(text)
        scores = data.get("attributeScores", {})
        values = []
        for key in ("TOXICITY", "INSULT", "THREAT"):
            value = scores.get(key, {}).get("summaryScore", {}).get("value")
            if value is not None:
                values.append(float(value))
        return any(score >= threshold for score in values)
