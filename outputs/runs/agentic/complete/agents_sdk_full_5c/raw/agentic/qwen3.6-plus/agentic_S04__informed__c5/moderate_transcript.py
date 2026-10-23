"""
Moderate transcript text before publishing using Azure AI Content Safety.

Analyzes transcript segments for harmful content (hate, violence, sexual,
self-harm) using the Azure AI Content Safety API before allowing publication.
"""

import os
import base64
from typing import List, Optional, Dict, Tuple

import requests

from speech_models import TranscriptionSegment, TranscriptionResult


CONTENT_SAFETY_CATEGORIES = [
    "Hate",
    "Sexual",
    "Violence",
    "SelfHarm",
]


def get_content_safety_config() -> Tuple[str, str]:
    """
    Load Azure AI Content Safety credentials from environment variables.

    Returns:
        Tuple of (endpoint_url, api_key).

    Raises:
        EnvironmentError: If required credentials are not set.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )
    if not key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required"
        )

    return endpoint, key


def analyze_text(
    text: str,
    output_type: str = "EightSeverityLevels",
) -> dict:
    """
    Analyze a single text string for harmful content via Azure AI Content Safety.

    Azure AI Content Safety evaluates text across four harm categories:
    Hate, Sexual, Violence, and SelfHarm, returning severity levels from 0-7.

    Args:
        text: The text content to analyze.
        output_type: Response format ('FourSeverityLevels' or 'EightSeverityLevels').

    Returns:
        Raw JSON response from Azure AI Content Safety API.

    Raises:
        requests.HTTPError: If the Azure API returns an error.
    """
    endpoint, key = get_content_safety_config()
    api_version = "2024-02-15-preview"

    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "outputType": output_type,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()


def check_segment_safety(
    segment: TranscriptionSegment,
    severity_threshold: int = 4,
) -> Tuple[bool, Dict[str, int]]:
    """
    Check whether a single transcript segment passes content safety moderation.

    Args:
        segment: The TranscriptionSegment to analyze.
        severity_threshold: Maximum allowed severity level (0-7) per category.

    Returns:
        Tuple of (is_safe, dict of category -> severity levels).
    """
    result = analyze_text(segment.text)

    category_severities = {}
    is_safe = True

    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        category_severities[category] = severity

        if severity >= severity_threshold:
            is_safe = False

    return is_safe, category_severities


def moderate_transcript_segments(
    segments: List[TranscriptionSegment],
    severity_threshold: int = 4,
    flag_only: bool = True,
) -> List[Dict]:
    """
    Moderate a list of transcript segments using Azure AI Content Safety.

    Each segment is analyzed and flagged if it exceeds the severity threshold
    in any harm category (Hate, Sexual, Violence, SelfHarm).

    Args:
        segments: List of TranscriptionSegment to moderate.
        severity_threshold: Max allowed severity level per category.
        flag_only: If True, keep all segments but add safety flags.
                   If False, exclude unsafe segments from results.

    Returns:
        List of dicts with segment data and safety analysis results.
    """
    results = []

    for segment in segments:
        is_safe, category_severities = check_segment_safety(
            segment, severity_threshold
        )

        result_entry = {
            "segment": segment,
            "is_safe": is_safe,
            "category_severities": category_severities,
            "action": "flagged" if not is_safe else "approved",
        }

        if flag_only or is_safe:
            results.append(result_entry)

    return results


def moderate_transcript(
    transcript_result: TranscriptionResult,
    severity_threshold: int = 4,
) -> Dict:
    """
    Full workflow: moderate an entire transcript using Azure AI Content Safety.

    Analyzes every segment and returns a summary with approval status,
    flagged segments, and overall risk assessment.

    Args:
        transcript_result: The TranscriptionResult to moderate.
        severity_threshold: Maximum allowed severity per category.

    Returns:
        Dictionary with moderation summary including:
        - overall_safe: bool
        - total_segments: int
        - flagged_count: int
        - flagged_segments: list of problematic segments
        - category_max_severity: dict of highest severity per category
    """
    moderation_results = moderate_transcript_segments(
        transcript_result.segments,
        severity_threshold=severity_threshold,
    )

    flagged = [r for r in moderation_results if not r["is_safe"]]

    category_max = {}
    for result in moderation_results:
        for cat, sev in result["category_severities"].items():
            if cat not in category_max or sev > category_max[cat]:
                category_max[cat] = sev

    overall_safe = len(flagged) == 0

    return {
        "overall_safe": overall_safe,
        "total_segments": len(moderation_results),
        "flagged_count": len(flagged),
        "flagged_segments": [
            {
                "text": r["segment"].text,
                "speaker": r["segment"].speaker_label,
                "severities": r["category_severities"],
            }
            for r in flagged
        ],
        "category_max_severity": category_max,
    }
