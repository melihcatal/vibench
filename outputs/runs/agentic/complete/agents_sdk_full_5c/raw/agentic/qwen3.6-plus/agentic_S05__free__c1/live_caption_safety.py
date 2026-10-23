"""Check live transcript text for unsafe content using Google Cloud Perspective API.

Uses the Google Perspective API (commentanalyzer.googleapis.com) to analyze
live transcript text for toxicity and other safety attributes.
"""

import os
from typing import Dict, List, Optional, Tuple

import requests

from speech_models import clean_transcript_text

# Google Perspective API endpoint
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

# Default safety attributes to check via Perspective API
DEFAULT_SAFETY_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "IDENTITY_ATTACK",
]


def get_perspective_api_key() -> str:
    """Retrieve the Google Perspective API key from environment.

    Returns:
        API key string.

    Raises:
        ValueError: If PERSPECTIVE_API_KEY environment variable is not set.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "PERSPECTIVE_API_KEY environment variable must be set "
            "for Google Perspective API access."
        )
    return api_key


def analyze_text_safety(
    text: str,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
) -> Dict[str, float]:
    """Analyze text for unsafe content using the Google Perspective API.

    Sends the text to commentanalyzer.googleapis.com and returns score
    mappings for each requested safety attribute.

    Args:
        text: The text to analyze for safety concerns.
        attributes: List of Perspective API attribute names to check.
            Defaults to DEFAULT_SAFETY_ATTRIBUTES.
        languages: List of language codes for the text. Defaults to ["en"].

    Returns:
        Dictionary mapping attribute names to their toxicity/safety scores (0.0-1.0).
    """
    api_key = get_perspective_api_key()
    attributes = attributes or DEFAULT_SAFETY_ATTRIBUTES
    languages = languages or ["en"]

    attribute_params = {attr: {} for attr in attributes}

    payload = {
        "comment": {"text": text},
        "requestedAttributes": attribute_params,
        "languages": languages,
        "doNotStore": True,
        "clientToken": "live-caption-safety-checker",
    }

    response = requests.post(
        PERSPECTIVE_API_ENDPOINT,
        params={"key": api_key},
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()

    result = response.json()
    scores = {}
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        summary = attr_data.get("summaryScore", {})
        scores[attr_name] = summary.get("value", 0.0)

    return scores


def check_transcript_safety(
    transcript: str,
    threshold: float = 0.7,
    attributes: Optional[List[str]] = None,
) -> Tuple[bool, Dict[str, float]]:
    """Check if a transcript exceeds safety thresholds using Perspective API.

    Args:
        transcript: The transcript text to check.
        threshold: Score threshold above which content is flagged as unsafe.
        attributes: Safety attributes to check.

    Returns:
        Tuple of (is_unsafe, attribute_scores).
    """
    cleaned = clean_transcript_text(transcript)
    if not cleaned:
        return False, {}

    scores = analyze_text_safety(cleaned, attributes=attributes)

    is_unsafe = any(score >= threshold for score in scores.values())
    return is_unsafe, scores


def monitor_streaming_safety(
    transcript_events,
    threshold: float = 0.7,
    attributes: Optional[List[str]] = None,
):
    """Monitor a stream of recognition events for unsafe content.

    Checks each final transcript against the Perspective API safety model
    and yields safety alerts when thresholds are exceeded.

    Args:
        transcript_events: Iterator of (transcript, is_final, confidence) tuples.
        threshold: Safety score threshold.
        attributes: Safety attributes to check.

    Yields:
        Tuples of (transcript, is_unsafe, flagged_attributes, scores) for final results.
    """
    for transcript, is_final, confidence in transcript_events:
        if not is_final:
            continue

        is_unsafe, scores = check_transcript_safety(
            transcript,
            threshold=threshold,
            attributes=attributes,
        )

        if is_unsafe:
            flagged = [attr for attr, score in scores.items() if score >= threshold]
            yield transcript, True, flagged, scores
        else:
            yield transcript, False, [], scores
