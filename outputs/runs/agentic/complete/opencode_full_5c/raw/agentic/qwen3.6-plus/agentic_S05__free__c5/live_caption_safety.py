import asyncio
import os
import re
from dataclasses import dataclass, field
from typing import AsyncGenerator, Dict, List, Optional
from urllib.parse import urlencode

import aiohttp

from speech_models import StreamingTranscriptEvent

PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)
PERSPECTIVE_API_KEY_ENV = "PERSPECTIVE_API_KEY"


@dataclass
class SafetyScore:
    category: str
    score: float
    threshold: float = 0.7

    @property
    def is_unsafe(self) -> bool:
        return self.score >= self.threshold


@dataclass
class SafetyAnalysisResult:
    text: str
    scores: List[SafetyScore]
    overall_safe: bool
    flagged_categories: List[str]
    timestamp: str = ""


class LiveCaptionSafetyChecker:
    DEFAULT_CATEGORIES = [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "INSULT",
        "PROFANITY",
        "THREAT",
        "SEXUALLY_EXPLICIT",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        threshold: float = 0.7,
        categories: Optional[List[str]] = None,
    ):
        self.api_key = api_key or os.environ.get(PERSPECTIVE_API_KEY_ENV, "")
        self.threshold = threshold
        self.categories = categories or self.DEFAULT_CATEGORIES
        self._session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def analyze_text(self, text: str) -> SafetyAnalysisResult:
        if not text or not text.strip():
            return SafetyAnalysisResult(
                text=text,
                scores=[],
                overall_safe=True,
                flagged_categories=[],
            )

        session = await self._ensure_session()

        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {cat: {} for cat in self.categories},
        }

        params = {"key": self.api_key}
        url = f"{PERSPECTIVE_API_ENDPOINT}?{urlencode(params)}"

        async with session.post(url, json=payload) as response:
            data = await response.json()

        scores = []
        flagged = []
        attribute_scores = data.get("attributeScores", {})

        for category in self.categories:
            attr_data = attribute_scores.get(category, {})
            score_summary = attr_data.get("summaryScore", {})
            score_value = score_summary.get("value", 0.0)
            score_obj = SafetyScore(
                category=category,
                score=score_value,
                threshold=self.threshold,
            )
            scores.append(score_obj)
            if score_obj.is_unsafe:
                flagged.append(category)

        return SafetyAnalysisResult(
            text=text,
            scores=scores,
            overall_safe=len(flagged) == 0,
            flagged_categories=flagged,
        )

    async def check_event(
        self, event: StreamingTranscriptEvent
    ) -> SafetyAnalysisResult:
        result = await self.analyze_text(event.text)
        result.timestamp = event.timestamp.isoformat()
        return result

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()


async def live_caption_safety(
    transcript_events: AsyncGenerator[StreamingTranscriptEvent, None],
    threshold: float = 0.7,
    categories: Optional[List[str]] = None,
) -> AsyncGenerator[SafetyAnalysisResult, None]:
    checker = LiveCaptionSafetyChecker(threshold=threshold, categories=categories)
    try:
        async for event in transcript_events:
            if event.text:
                result = await checker.check_event(event)
                yield result
    finally:
        await checker.close()


async def filter_unsafe_captions(
    transcript_events: AsyncGenerator[StreamingTranscriptEvent, None],
    threshold: float = 0.8,
) -> AsyncGenerator[StreamingTranscriptEvent, None]:
    checker = LiveCaptionSafetyChecker(threshold=threshold)
    try:
        async for event in transcript_events:
            if event.text:
                safety = await checker.check_event(event)
                if safety.overall_safe:
                    yield event
    finally:
        await checker.close()
