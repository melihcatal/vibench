"""Check generated visual labels for unsafe text using Perspective API.

Provider: Perspective API
SDK: requests
Auth: PERSPECTIVE_API_KEY
"""

import json
import os
from typing import Dict, List, Optional

import requests


PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def _build_perspective_payload(
    text: str,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
) -> dict:
    """Build the JSON payload for a Perspective API analyze request."""
    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
            "IDENTITY_ATTACK",
        ]
    if languages is None:
        languages = ["en"]

    return {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
    }


def check_visual_labels_safety(
    labels_text: str,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
) -> Dict[str, float]:
    """Check visual labels / description text for unsafe content via Perspective API.

    Args:
        labels_text: The combined label or description text to evaluate.
        api_key: Perspective API key. Falls back to PERSPECTIVE_API_KEY env var.
        attributes: List of Perspective API attributes to score.

    Returns:
        A dict mapping attribute names to their toxicity scores (0.0 - 1.0).
    """
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY", "")
    if not key:
        raise ValueError(
            "Perspective API key is required. Set PERSPECTIVE_API_KEY env var."
        )

    payload = _build_perspective_payload(labels_text, attributes=attributes)

    params = {"key": key}
    response = requests.post(
        PERSPECTIVE_API_ENDPOINT,
        params=params,
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()

    result = response.json()
    scores = {}
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        score_data = attr_data.get("summaryScore", {})
        scores[attr_name] = score_data.get("value", 0.0)

    return scores


def is_visual_text_safe(
    scores: Dict[str, float],
    threshold: float = 0.7,
) -> bool:
    """Determine if the visual labels text is safe based on Perspective API scores.

    Args:
        scores: Dict of attribute names to scores from check_visual_labels_safety.
        threshold: Score threshold above which text is considered unsafe.

    Returns:
        True if all scores are below the threshold (safe), False otherwise.
    """
    return all(score < threshold for score in scores.values())


def run_visual_safety_text(
    labels_text: str,
    api_key: Optional[str] = None,
) -> dict:
    """Run visual labels safety check and return a structured result.

    Args:
        labels_text: The text to evaluate (e.g., detected labels concatenated).
        api_key: Optional Perspective API key.

    Returns:
        A dict with scores, safety flag, and provider metadata.
    """
    scores = check_visual_labels_safety(labels_text, api_key=api_key)
    safe = is_visual_text_safe(scores)

    return {
        "provider": "perspective-api",
        "model": "perspective-v1alpha1",
        "input_text": labels_text,
        "scores": scores,
        "is_safe": safe,
    }


if __name__ == "__main__":
    sample_text = os.environ.get(
        "LABELS_TEXT",
        "outdoor, sky, building, street, nature",
    )
    result = run_visual_safety_text(sample_text)
    print(result)
