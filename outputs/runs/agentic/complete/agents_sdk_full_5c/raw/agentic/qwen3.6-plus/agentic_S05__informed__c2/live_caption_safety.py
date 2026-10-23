"""
Check live transcript text for unsafe content using Google Perspective API.
Analyzes streaming transcript chunks for toxicity, profanity, and other safety attributes.

Provider: Google Perspective API
SDK: requests (REST API)
Auth: PERSPECTIVE_API_KEY
"""

import logging
from typing import Optional

import requests

from speech_models import FinalTranscriptResult

logger = logging.getLogger(__name__)

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

# Default attributes to check
DEFAULT_SAFETY_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
]


class LiveCaptionSafetyChecker:
    """
    Checks live caption text for unsafe content using Perspective API.

    Provides configurable toxicity and safety attribute scoring for
    streaming transcript moderation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        attributes: Optional[list[str]] = None,
        threshold: float = 0.7,
        languages: Optional[list[str]] = None,
    ):
        """
        Initialize the Perspective API safety checker.

        Args:
            api_key: Perspective API key. Falls back to PERSPECTIVE_API_KEY env var.
            attributes: List of attributes to check (default: DEFAULT_SAFETY_ATTRIBUTES).
            threshold: Score threshold above which content is flagged (0.0 to 1.0).
            languages: List of BCP-47 language codes for analysis.
        """
        self.api_key = api_key
        if not self.api_key:
            import os
            self.api_key = os.environ.get("PERSPECTIVE_API_KEY")

        self.attributes = attributes or DEFAULT_SAFETY_ATTRIBUTES
        self.threshold = threshold
        self.languages = languages or ["en"]

        if not self.api_key:
            logger.warning("PERSPECTIVE_API_KEY not set. Safety checks will fail.")

    def analyze_text(self, text: str) -> dict:
        """
        Analyze text using the Perspective API.

        Args:
            text: Text to analyze for safety.

        Returns:
            Dict with attribute scores and flagged status.
        """
        if not text or not text.strip():
            return {"text": text, "flagged": False, "scores": {}, "attributes": {}}

        if not self.api_key:
            logger.error("No Perspective API key configured")
            return {"text": text, "flagged": False, "scores": {}, "attributes": {}, "error": "no_api_key"}

        requested_attributes = {attr: {} for attr in self.attributes}

        payload = {
            "comment": {"text": text},
            "requestedAttributes": requested_attributes,
            "languages": self.languages,
            "doNotStore": True,
        }

        try:
            response = requests.post(
                PERSPECTIVE_API_URL,
                params={"key": self.api_key},
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as e:
            logger.error(f"Perspective API request failed: {e}")
            return {"text": text, "flagged": False, "scores": {}, "attributes": {}, "error": str(e)}

        scores = {}
        flagged = False
        for attr_name, attr_data in result.get("attributeScores", {}).items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            scores[attr_name] = score
            if score >= self.threshold:
                flagged = True

        return {
            "text": text,
            "flagged": flagged,
            "scores": scores,
            "threshold": self.threshold,
        }

    def check_final_result(self, result: FinalTranscriptResult) -> dict:
        """
        Check a FinalTranscriptResult for unsafe content.

        Args:
            result: FinalTranscriptResult to check.

        Returns:
            Dict with safety analysis results.
        """
        analysis = self.analyze_text(result.transcript)
        analysis["transcript_confidence"] = result.confidence
        return analysis

    def is_safe(self, text: str) -> bool:
        """
        Quick check if text is safe (below threshold for all attributes).

        Args:
            text: Text to check.

        Returns:
            True if text is safe, False if any attribute exceeds threshold.
        """
        result = self.analyze_text(text)
        return not result.get("flagged", True)


def create_safety_checker(
    api_key: Optional[str] = None,
    threshold: float = 0.7,
    attributes: Optional[list[str]] = None,
) -> LiveCaptionSafetyChecker:
    """
    Factory function to create a Perspective API safety checker.

    Args:
        api_key: Perspective API key.
        threshold: Score threshold for flagging.
        attributes: List of attributes to check.

    Returns:
        Configured LiveCaptionSafetyChecker instance.
    """
    return LiveCaptionSafetyChecker(
        api_key=api_key,
        threshold=threshold,
        attributes=attributes,
    )
