"""
Moderate transcript text before publishing using Google Perspective API.

Analyzes transcript content for toxic, profane, or harmful language
using Perspective API's toxicity and safety models.
Requires PERSPECTIVE_API_KEY environment variable.
"""

import os
import sys
from typing import List, Optional, Dict, Any

import requests


# Perspective API provider identifiers
PROVIDER = "Perspective API"
PROVIDER_API_HOST = "commentanalyzer.googleapis.com"
PROVIDER_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class PerspectiveModerator:
    """Wrapper for Google Perspective API content moderation."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Perspective API client.

        Args:
            api_key: Perspective API key. Defaults to PERSPECTIVE_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "PERSPECTIVE_API_KEY environment variable must be set "
                "to use Perspective API"
            )

    def analyze_text(
        self,
        text: str,
        attributes: Optional[List[str]] = None,
        languages: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze text using Perspective API safety attributes.

        Args:
            text: Text to analyze.
            attributes: List of attributes to check (default: TOXICITY, SEVERE_TOXICITY).
            languages: List of language codes (default: ['en']).

        Returns:
            Dict with analysis results per attribute.
        """
        if attributes is None:
            attributes = ["TOXICITY", "SEVERE_TOXICITY", "PROFANITY", "THREAT"]

        if languages is None:
            languages = ["en"]

        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                attr: {} for attr in attributes
            },
            "languages": languages,
            "spanAnnotations": False,
        }

        params = {"key": self.api_key}

        response = requests.post(
            PROVIDER_API_URL,
            json=payload,
            params=params,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        return response.json()

    def moderate_segments(
        self,
        segments: List[str],
        attributes: Optional[List[str]] = None,
        threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """
        Moderate multiple transcript segments.

        Args:
            segments: List of text segments to moderate.
            attributes: Attributes to check.
            threshold: Score threshold for flagging (0.0-1.0).

        Returns:
            List of moderation results for each segment.
        """
        results = []
        for segment in segments:
            if not segment.strip():
                continue

            try:
                analysis = self.analyze_text(segment, attributes=attributes)
                flagged = False
                scores = {}

                attr_scores = analysis.get("attributeScores", {})
                for attr_name, attr_data in attr_scores.items():
                    score = attr_data.get("summaryScore", {}).get("value", 0.0)
                    scores[attr_name] = score
                    if score >= threshold:
                        flagged = True

                results.append({
                    "text": segment,
                    "flagged": flagged,
                    "scores": scores,
                    "threshold": threshold,
                })
            except Exception as e:
                results.append({
                    "text": segment,
                    "error": str(e),
                    "flagged": True,  # Conservative: flag on error
                })

        return results


def moderate_transcript(
    transcript_text: str,
    threshold: float = 0.7,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate an entire transcript using Perspective API.

    Analyzes the full transcript text for toxicity and harmful content.

    Args:
        transcript_text: Full transcript text to moderate.
        threshold: Score threshold for flagging (0.0-1.0).
        api_key: Optional Perspective API key override.

    Returns:
        Dict with moderation results including flagged status and scores.
    """
    moderator = PerspectiveModerator(api_key=api_key)
    analysis = moderator.analyze_text(transcript_text)

    flagged = False
    scores = {}

    attr_scores = analysis.get("attributeScores", {})
    for attr_name, attr_data in attr_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flagged = True

    return {
        "text_length": len(transcript_text),
        "flagged": flagged,
        "scores": scores,
        "threshold": threshold,
        "provider": PROVIDER,
    }


def moderate_transcript_segments(
    segments: List[str],
    threshold: float = 0.7,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Moderate transcript segments individually.

    Args:
        segments: List of transcript segments.
        threshold: Score threshold for flagging.
        api_key: Optional Perspective API key override.

    Returns:
        List of moderation results per segment.
    """
    moderator = PerspectiveModerator(api_key=api_key)
    return moderator.moderate_segments(
        segments,
        threshold=threshold,
    )


if __name__ == "__main__":
    # Example usage
    sample_text = "This is a clean, professional meeting transcript."
    result = moderate_transcript(sample_text)
    print(f"Flagged: {result['flagged']}")
    print(f"Scores: {result['scores']}")
