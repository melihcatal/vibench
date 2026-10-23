"""
Moderate free-text claims or notes using the Perspective API.

Provider: Google Perspective API
Environment variable: PERSPECTIVE_API_KEY

Analyzes user-submitted free-text claims, notes, or profile information
for toxicity, profanity, and other harmful content attributes using
the Google Perspective API.
"""

from __future__ import annotations

import os
from typing import Optional

import requests


class PerspectiveModerator:
    """Moderates text content using the Google Perspective API."""

    PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    DEFAULT_ATTRIBUTES = [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "IDENTITY_ATTACK",
        "INSULT",
        "PROFANITY",
        "THREAT",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        threshold: float = 0.7,
    ):
        self.api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY", "")
        self.threshold = threshold

    def moderate(
        self,
        text: str,
        language: str = "en",
        attributes: Optional[list[str]] = None,
    ) -> dict:
        """
        Moderate a text string using the Perspective API.

        Args:
            text: The text content to moderate
            language: BCP-47 language code (default: "en")
            attributes: List of attributes to check (default: TOXICITY, etc.)

        Returns:
            Dict with 'moderated': bool, 'scores': dict of attribute scores,
            'flags': list of flagged attributes, and 'raw_response': API response
        """
        if not self.api_key:
            raise ValueError(
                "Perspective API key is required. Set PERSPECTIVE_API_KEY."
            )

        requested_attributes = {
            attr: {} for attr in (attributes or self.DEFAULT_ATTRIBUTES)
        }

        payload = {
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": requested_attributes,
        }

        params = {"key": self.api_key}

        response = requests.post(
            self.PERSPECTIVE_API_URL,
            json=payload,
            params=params,
            timeout=30,
        )

        if response.status_code != 200:
            raise PerspectiveModerationError(
                f"Perspective API request failed: {response.status_code} {response.text}",
                status_code=response.status_code,
            )

        result = response.json()
        return self._parse_response(result)

    def moderate_batch(
        self,
        texts: list[str],
        language: str = "en",
    ) -> list[dict]:
        """
        Moderate multiple text strings using the Perspective API.

        Returns a list of moderation results, one per input text.
        """
        results = []
        for text in texts:
            try:
                result = self.moderate(text, language=language)
                results.append(result)
            except PerspectiveModerationError as e:
                results.append({
                    "error": str(e),
                    "moderated": True,
                    "scores": {},
                    "flags": [],
                })
        return results

    def is_safe(self, text: str, language: str = "en") -> bool:
        """
        Check if a text is safe (no flagged attributes above threshold).
        """
        result = self.moderate(text, language=language)
        return not result["flags"]

    def _parse_response(self, response: dict) -> dict:
        """Parse the Perspective API response into a standardized format."""
        attribute_scores = response.get("attributeScores", {})
        scores = {}
        flags = []

        for attr_name, attr_data in attribute_scores.items():
            summary = attr_data.get("summaryScore", {})
            score = summary.get("value", 0.0)
            scores[attr_name] = score
            if score >= self.threshold:
                flags.append(attr_name)

        return {
            "moderated": True,
            "scores": scores,
            "flags": flags,
            "is_safe": len(flags) == 0,
            "raw_response": response,
        }


class PerspectiveModerationError(Exception):
    """Raised when Perspective API moderation fails."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def moderate_claim_text(
    text: str,
    api_key: Optional[str] = None,
    threshold: float = 0.7,
) -> dict:
    """
    Convenience function to moderate a free-text claim using Perspective API.

    Returns a moderation result dict with scores and flags.
    """
    moderator = PerspectiveModerator(api_key=api_key, threshold=threshold)
    return moderator.moderate(text)


def check_claim_safety(
    text: str,
    api_key: Optional[str] = None,
    threshold: float = 0.7,
) -> bool:
    """
    Convenience function to check if a claim text is safe.

    Returns True if no attributes exceed the threshold.
    """
    moderator = PerspectiveModerator(api_key=api_key, threshold=threshold)
    return moderator.is_safe(text)


if __name__ == "__main__":
    sample_text = "This is a harmless user profile note."
    result = moderate_claim_text(sample_text)
    print(f"Safe: {result['is_safe']}")
    print(f"Scores: {result['scores']}")
    print(f"Flags: {result['flags']}")
