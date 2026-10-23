"""
visual_safety_text.py - Check generated visual labels for unsafe text
using Azure AI Content Safety (azure-ai-contentsafety SDK / REST).

Provider: Azure AI Content Safety
SDK: requests (REST endpoint)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Optional

import requests

from vision_models import (
    LabelDetectionResponse,
    SafetyScoreResponse,
)

# Azure AI Content Safety text analysis endpoint pattern
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_visual_labels_safety(
    label_response: LabelDetectionResponse,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[List[str]] = None,
) -> SafetyScoreResponse:
    """Check detected image labels for unsafe text using Azure AI Content Safety.

    Combines all detected label descriptions and runs them through Azure's
    text moderation API (Analyze Text).

    Args:
        label_response: The label detection results from detect_image_labels.py.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.
        categories: Optional list of text categories to check
                    (Hate, SelfHarm, Sexual, Violence).

    Returns:
        SafetyScoreResponse with text-based safety ratings for the labels.
    """
    if not label_response.labels:
        return SafetyScoreResponse(
            ratings=[],
            is_safe=True,
            flagged_categories=[],
            raw_response={"status": "ok", "provider": "azure-ai-content-safety"},
        )

    # Build text input from all detected labels
    label_texts = [lbl.label for lbl in label_response.labels]
    input_text = ", ".join(label_texts)

    endpoint_url = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    api_key_value = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not endpoint_url:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required."
        )
    if not api_key_value:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required."
        )

    # Build the Analyze Text request for Azure AI Content Safety
    analysis_url = (
        f"{endpoint_url}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    )

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key_value,
    }

    check_categories = categories or ["Hate", "SelfHarm", "Sexual", "Violence"]

    payload: Dict[str, Any] = {
        "text": input_text,
        "categories": check_categories,
        "outputType": "EightSeverityLevels",
    }

    resp = requests.post(analysis_url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()

    ratings = []
    flagged = []
    is_safe = True

    category_results = data.get("categoriesAnalysis", [])
    for cat_result in category_results:
        cat_name = cat_result.get("category", "unknown")
        severity = cat_result.get("severity", 0)

        # Map Azure severity (0-7) to likelihood string and score
        likelihood_map = {
            0: ("NoIssue", 0.0),
            1: ("NoIssue", 0.0),
            2: ("Unlikely", 0.15),
            3: ("Possible", 0.35),
            4: ("Likely", 0.6),
            5: ("Likely", 0.7),
            6: ("VeryLikely", 0.85),
            7: ("VeryLikely", 1.0),
        }
        likelihood_str, score = likelihood_map.get(severity, ("Unknown", 0.5))

        rating = SafetyScoreResponse.__annotations__
        from vision_models import SafetyRating
        rating_obj = SafetyRating(
            category=cat_name.lower(),
            likelihood=likelihood_str,
            likelihood_score=score,
        )
        ratings.append(rating_obj)

        if score >= 0.5:
            flagged.append(cat_name.lower())
            is_safe = False

    return SafetyScoreResponse(
        ratings=ratings,
        is_safe=is_safe,
        flagged_categories=flagged,
        raw_response={
            "status": "ok",
            "provider": "azure-ai-content-safety",
            "response_data": data,
        },
    )


def check_visual_labels_safety_from_file(
    label_response: LabelDetectionResponse,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> SafetyScoreResponse:
    """Wrapper using environment variables for Azure AI Content Safety."""
    return check_visual_labels_safety(
        label_response=label_response,
        endpoint=endpoint,
        api_key=api_key,
    )


def format_visual_safety_text_report(response: SafetyScoreResponse) -> str:
    """Format a human-readable text safety report for visual labels."""
    lines = [
        "=== Visual Labels Text Safety Report (Azure AI Content Safety) ===",
        "",
        f"Overall Safe: {response.is_safe}",
        f"Flagged Categories: {', '.join(response.flagged_categories) if response.flagged_categories else 'none'}",
        "",
        "Category Ratings:",
    ]
    for rating in response.ratings:
        score = rating.likelihood_score if rating.likelihood_score is not None else 0.0
        lines.append(
            f"  - {rating.category}: {rating.likelihood} (score: {score:.2f})"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo with sample label data
    from vision_models import LabelResult

    sample_labels = LabelDetectionResponse(
        labels=[
            LabelResult(label="person", confidence=0.95),
            LabelResult(label="building", confidence=0.88),
            LabelResult(label="vehicle", confidence=0.76),
            LabelResult(label="street", confidence=0.72),
        ],
        raw_response={"provider": "google-cloud-vision"},
    )

    try:
        result = check_visual_labels_safety_from_file(sample_labels)
        print(format_visual_safety_text_report(result))
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to run.")
