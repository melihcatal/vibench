import os
from typing import AsyncIterator

import requests
from googleapiclient.discovery import build

from speech_models import StreamingResult, StreamingEvent


class LiveCaptionSafetyChecker:
    def __init__(
        self,
        api_key: str | None = None,
        threshold: float = 0.7,
        categories: list[str] | None = None,
    ):
        self.api_key = api_key or os.getenv("PERSPECTIVE_API_KEY", "")
        self.threshold = threshold
        self.categories = categories or [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
        ]
        self._api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_text(self, text: str) -> dict:
        if not text.strip():
            return {"flagged": False, "scores": {}}

        params = {"key": self.api_key}
        payload = {
            "comment": {"text": text},
            "requested_attributes": {cat: {} for cat in self.categories},
            "languages": ["en"],
        }

        response = requests.post(self._api_url, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        scores = {}
        flagged = False
        attribute_scores = data.get("attributeScores", {})
        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            scores[attr_name] = score
            if score >= self.threshold:
                flagged = True

        return {"flagged": flagged, "scores": scores}

    def check_event(self, event: StreamingEvent) -> StreamingEvent:
        if event.result is None or not event.result.transcript.strip():
            event.metadata["safety"] = {"flagged": False, "scores": {}}
            return event

        safety_result = self.check_text(event.result.transcript)
        event.metadata["safety"] = safety_result
        return event


async def live_caption_safety(
    transcript_events: AsyncIterator[StreamingEvent],
    api_key: str | None = None,
    threshold: float = 0.7,
    categories: list[str] | None = None,
) -> AsyncIterator[StreamingEvent]:
    checker = LiveCaptionSafetyChecker(
        api_key=api_key,
        threshold=threshold,
        categories=categories,
    )
    async for event in transcript_events:
        checked = checker.check_event(event)
        yield checked
