"""
Check live transcript text for unsafe content using the Google Perspective API.

This module sends live transcription text to the Google Perspective API
(endpoint: commentanalyzer.googleapis.com) to analyze content for toxicity,
profanity, threat, and other safety attributes. Results are scored on a
0.0-1.0 scale per attribute, allowing real-time content moderation of
streaming speech recognition output.
"""

import asyncio
import json
import logging
import os
from typing import AsyncIterator, Optional

import aiohttp

logger = logging.getLogger(__name__)

PERSPECTIVE_API_ENDPOINT = "commentanalyzer.googleapis.com"
PERSPECTIVE_API_URL = f"https://{PERSPECTIVE_API_ENDPOINT}/v1alpha1/comments:analyze"
DEFAULT_PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "PROFANITY",
    "THREAT",
    "INSULT",
    "IDENTITY_ATTACK",
]


class ContentSafetyResult:
    """Result from a Perspective API safety analysis."""

    def __init__(self, text: str, scores: dict, flagged: bool, flagging_attributes: list[str]):
        self.text = text
        self.scores = scores
        self.flagged = flagged
        self.flagging_attributes = flagging_attributes

    @property
    def max_toxicity_score(self) -> float:
        """Return the highest toxicity-related score."""
        toxicity_keys = ["TOXICITY", "SEVERE_TOXICITY"]
        return max(
            (self.scores.get(k, 0.0) for k in toxicity_keys),
            default=0.0,
        )

    def is_safe(self, threshold: float = 0.7) -> bool:
        """Check if content is safe below the given threshold."""
        return not self.flagged or self.max_toxicity_score < threshold

    def to_dict(self) -> dict:
        """Convert to a serializable dictionary."""
        return {
            "text": self.text,
            "scores": self.scores,
            "flagged": self.flagged,
            "flagging_attributes": self.flagging_attributes,
            "max_toxicity_score": self.max_toxicity_score,
            "is_safe": self.is_safe(),
        }


class LiveCaptionSafetyChecker:
    """
    Check live caption text for unsafe content using Google Perspective API.

    Connects to commentanalyzer.googleapis.com to score text for toxicity,
    profanity, threats, and other harmful content attributes. Designed for
    real-time moderation of streaming speech-to-text transcripts.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        attributes: Optional[list[str]] = None,
        languages: Optional[list[str]] = None,
        toxicity_threshold: float = 0.7,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """
        Initialize the safety checker.

        Args:
            api_key: Google API key for Perspective API access.
            attributes: List of safety attributes to analyze.
            languages: List of languages to analyze.
            toxicity_threshold: Score threshold above which content is flagged.
            session: Optional aiohttp session for HTTP requests.
        """
        self._api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY", "")
        self._attributes = attributes or DEFAULT_PERSPECTIVE_ATTRIBUTES
        self._languages = languages or ["en"]
        self._toxicity_threshold = toxicity_threshold
        self._session = session
        self._owns_session = session is None

        if not self._api_key:
            logger.warning(
                "PERSPECTIVE_API_KEY not set; Perspective API calls to %s will fail",
                PERSPECTIVE_API_ENDPOINT,
            )

        logger.info(
            "LiveCaptionSafetyChecker initialized for %s with attributes: %s",
            PERSPECTIVE_API_ENDPOINT,
            self._attributes,
        )

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def check_text(self, text: str) -> ContentSafetyResult:
        """
        Analyze text for unsafe content using the Perspective API.

        Sends the text to commentanalyzer.googleapis.com and returns
        scored safety attributes.

        Args:
            text: Caption text to analyze.

        Returns:
            ContentSafetyResult with attribute scores and flag status.
        """
        if not text or not text.strip():
            return ContentSafetyResult(
                text=text,
                scores={},
                flagged=False,
                flagging_attributes=[],
            )

        payload = {
            "comment": {"text": text},
            "languages": self._languages,
            "requestedAttributes": {
                attr: {} for attr in self._attributes
            },
        }

        params = {"key": self._api_key}

        session = await self._get_session()

        try:
            async with session.post(
                PERSPECTIVE_API_URL,
                params=params,
                json=payload,
            ) as response:
                response.raise_for_status()
                result_data = await response.json()

        except aiohttp.ClientError as exc:
            logger.error(
                "Perspective API request to %s failed: %s",
                PERSPECTIVE_API_ENDPOINT,
                exc,
            )
            return ContentSafetyResult(
                text=text,
                scores={},
                flagged=False,
                flagging_attributes=[],
            )

        scores = {}
        flagging_attributes = []

        attribute_scores = result_data.get("attributeScores", {})
        for attr_name, attr_data in attribute_scores.items():
            summary = attr_data.get("summaryScore", {})
            score = summary.get("value", 0.0)
            scores[attr_name] = score
            if score >= self._toxicity_threshold:
                flagging_attributes.append(attr_name)

        is_flagged = len(flagging_attributes) > 0

        logger.debug(
            "Perspective API analysis for text '%s' via %s: scores=%s, flagged=%s",
            text[:60],
            PERSPECTIVE_API_ENDPOINT,
            scores,
            is_flagged,
        )

        return ContentSafetyResult(
            text=text,
            scores=scores,
            flagged=is_flagged,
            flagging_attributes=flagging_attributes,
        )

    async def close(self) -> None:
        """Close the HTTP session if owned."""
        if self._owns_session and self._session:
            await self._session.close()
            self._session = None


async def stream_safety_check(
    caption_stream: AsyncIterator[dict],
    api_key: Optional[str] = None,
    toxicity_threshold: float = 0.7,
) -> AsyncIterator[dict]:
    """
    Consume a stream of live captions and yield safety analysis results.

    Args:
        caption_stream: Async iterator of caption dicts with 'text' key.
        api_key: Google Perspective API key.
        toxicity_threshold: Score threshold for flagging content.

    Yields:
        dict: Caption data enriched with safety analysis results.
    """
    checker = LiveCaptionSafetyChecker(
        api_key=api_key,
        toxicity_threshold=toxicity_threshold,
    )

    try:
        async for caption in caption_stream:
            text = caption.get("text", "")
            safety_result = await checker.check_text(text)

            enriched = {
                **caption,
                "safety": safety_result.to_dict(),
            }
            yield enriched
    finally:
        await checker.close()
