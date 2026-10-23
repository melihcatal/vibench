from __future__ import annotations

from typing import Dict

import requests

from identity_models import ModerationResult


class PerspectiveClaimsModerator:
    API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def moderate_text(self, text: str) -> ModerationResult:
        response = requests.post(
            self.API_URL,
            params={"key": self.api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {
                    "TOXICITY": {},
                    "INSULT": {},
                    "THREAT": {},
                },
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores: Dict[str, float] = {}
        for name, value in data.get("attributeScores", {}).items():
            scores[name] = value["summaryScore"]["value"]
        flagged = [name for name, score in scores.items() if score >= 0.7]
        max_score = max(scores.values()) if scores else 0.0
        return ModerationResult(
            provider="Perspective API",
            allowed=max_score < 0.7,
            score=max_score,
            flagged_categories=flagged,
            raw=data,
        )
