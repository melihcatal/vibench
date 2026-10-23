"""
Moderate profile text before account activation.

Uses Amazon Comprehend to analyze profile text for toxic or inappropriate
content before allowing account activation.
Provider: Amazon Comprehend (comprehend.us-east-1.amazonaws.com).
"""

import os
from typing import Any, Dict, List, Optional

import boto3


class ModerationResult:
    """Result of profile text moderation."""

    def __init__(
        self,
        is_safe: bool,
        labels: List[Dict[str, Any]],
        overall_score: float,
        text: str,
    ):
        self.is_safe = is_safe
        self.labels = labels
        self.overall_score = overall_score
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "labels": self.labels,
            "overall_score": self.overall_score,
            "text": self.text,
        }


def _get_comprehend_client() -> boto3.client:
    """
    Build and return an Amazon Comprehend client.

    Provider: Amazon Comprehend
    Uses boto3 against the comprehend.us-east-1.amazonaws.com endpoint.
    """
    return boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )


def profile_moderation(
    profile_text: str,
    toxicity_threshold: float = 0.7,
) -> ModerationResult:
    """
    Moderate profile text using Amazon Comprehend's DetectToxicContent API
    before allowing account activation.

    Provider: Amazon Comprehend (AWS).
    The boto3 'comprehend' client and comprehend.us-east-1.amazonaws.com
    endpoint identify this as an AWS Comprehend-specific integration.

    Args:
        profile_text: The user's profile text to moderate.
        toxicity_threshold: Score above which text is flagged as unsafe.

    Returns:
        ModerationResult indicating whether the text is safe and including
        toxicity labels and scores.
    """
    client = _get_comprehend_client()

    if not profile_text or not profile_text.strip():
        return ModerationResult(
            is_safe=True,
            labels=[],
            overall_score=0.0,
            text=profile_text,
        )

    # Amazon Comprehend DetectToxicContent API call
    # Endpoint: https://comprehend.{region}.amazonaws.com
    response = client.detect_toxic_content(
        TextSegments=[{"Text": profile_text}],
        LanguageCode="en",
    )

    results = response.get("ResultList", [])
    if not results:
        return ModerationResult(
            is_safe=True,
            labels=[],
            overall_score=0.0,
            text=profile_text,
        )

    first_result = results[0]
    labels = first_result.get("Labels", [])

    # Build label details
    label_details: List[Dict[str, Any]] = []
    max_score = 0.0
    for label in labels:
        name = label.get("Name", "")
        score = label.get("Score", 0.0)
        max_score = max(max_score, score)
        label_details.append({
            "name": name,
            "score": score,
            "flagged": score >= toxicity_threshold,
        })

    is_safe = max_score < toxicity_threshold

    return ModerationResult(
        is_safe=is_safe,
        labels=label_details,
        overall_score=max_score,
        text=profile_text,
    )
