from __future__ import annotations

from typing import Iterable

import requests

from speech_models import ModerationResult, normalize_transcript_text

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class LiveCaptionSafetyChecker:
    def __init__(self, api_key: str | None = None) -> None:
        import os

        self.api_key = api_key or os.getenv("PERSPECTIVE_API_KEY", "")

    def check_text(self, text: str) -> ModerationResult:
        payload = {
            "comment": {"text": normalize_transcript_text(text)},
            "requestedAttributes": {"TOXICITY": {}},
            "doNotStore": True,
        }
        params = {"key": self.api_key} if self.api_key else {}
        response = requests.post(PERSPECTIVE_URL, params=params, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        value = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        flagged = value >= 0.7
        return ModerationResult(flagged=flagged, score=float(value), categories=["TOXICITY"], raw=data)


def check_live_transcript_safety(chunks: Iterable[str], api_key: str | None = None) -> list[ModerationResult]:
    checker = LiveCaptionSafetyChecker(api_key)
    return [checker.check_text(chunk) for chunk in chunks if normalize_transcript_text(chunk)]
