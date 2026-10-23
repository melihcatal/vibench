"""
Check an image for unsafe or policy-sensitive visual content using Amazon Rekognition.

Provider: Amazon Rekognition (AWS)
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from typing import List, Optional, Union, Dict, Any
from pathlib import Path

from vision_client import (
    load_image_bytes,
    build_rekognition_image_payload,
    create_rekognition_client,
)
from vision_models import (
    SafetyModerationRequest,
    SafetyModerationResponse,
    SafetyCategory,
    normalize_rekognition_moderation,
    filter_by_confidence,
)


# Severity ordering for moderation labels
_SEVERITY_ORDER = [
    "NONE",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]

# Category-to-severity mapping used for Rekognition moderation taxonomy
_CATEGORY_SEVERITY = {
    "Explicit Nudity": "CRITICAL",
    "Suggestive": "HIGH",
    "Violence": "HIGH",
    "Visually Disturbing": "HIGH",
    "Rude Gestures": "MEDIUM",
    "Drugs": "HIGH",
    "Tobacco": "MEDIUM",
    "Alcohol": "MEDIUM",
    "Gambling": "MEDIUM",
    "Hate Symbols": "CRITICAL",
}


def score_image_safety(
    image_source: Union[str, bytes, Path],
    min_confidence: float = 0.5,
    categories: Optional[List[str]] = None,
    region: Optional[str] = None,
    custom_params: Optional[Dict[str, Any]] = None,
) -> SafetyModerationResponse:
    """
    Check an image for unsafe or policy-sensitive visual content using Amazon Rekognition.

    Uses the Rekognition DetectModerationLabels API to analyze visual content
    for policy violations including explicit content, violence, hate symbols,
    and other sensitive categories.

    Args:
        image_source: Path to image file, image bytes, or file-like object.
        min_confidence: Minimum confidence threshold for returned moderation labels.
        categories: Optional list of category names to filter by.
        region: AWS region override.
        custom_params: Additional parameters for the Rekognition API.

    Returns:
        SafetyModerationResponse with moderation labels and overall safety assessment.
    """
    client = create_rekognition_client(region)

    image_payload = build_rekognition_image_payload(image_source)

    rekognition_params: Dict[str, Any] = {
        "Image": image_payload,
        "MinConfidence": min_confidence,
    }

    if custom_params:
        rekognition_params.update(custom_params)

    raw_response = client.detect_moderation_labels(**rekognition_params)

    categories_list = normalize_rekognition_moderation(raw_response)

    # Filter by confidence
    categories_list = filter_by_confidence(categories_list, min_confidence)

    # Filter by specific categories if requested
    if categories:
        categories_list = [
            cat for cat in categories_list
            if cat.category in categories or cat.label in categories
        ]

    # Enrich with severity metadata
    highest_severity = "NONE"
    is_safe = True
    for cat in categories_list:
        severity = _CATEGORY_SEVERITY.get(cat.category, "LOW")
        cat.metadata["severity"] = severity
        if _SEVERITY_ORDER.index(severity) > _SEVERITY_ORDER.index(highest_severity):
            highest_severity = severity
            is_safe = False

    return SafetyModerationResponse(
        moderation_labels=categories_list,
        is_safe=is_safe,
        highest_severity=highest_severity,
        request_id=raw_response.get("ResponseMetadata", {}).get("RequestId", ""),
        raw_response=raw_response,
    )


def score_image_safety_from_request(
    request: SafetyModerationRequest,
    region: Optional[str] = None,
) -> SafetyModerationResponse:
    """
    Score image safety from a unified SafetyModerationRequest object.

    Args:
        request: A SafetyModerationRequest with image source and parameters.
        region: AWS region override.

    Returns:
        SafetyModerationResponse with moderation results.
    """
    return score_image_safety(
        image_source=request.image_source,
        min_confidence=request.min_confidence,
        categories=request.categories,
        region=region,
        custom_params=request.custom_params,
    )


def format_safety_summary(response: SafetyModerationResponse) -> str:
    """Format safety moderation results into a human-readable summary."""
    if response.is_safe:
        return "Image is SAFE — no policy-sensitive content detected."

    lines = [
        f"Image is UNSAFE — highest severity: {response.highest_severity}",
        "Moderation labels:",
    ]
    for cat in response.moderation_labels:
        severity = cat.metadata.get("severity", "UNKNOWN")
        parent_info = f" (parent: {cat.label})" if cat.label else ""
        lines.append(
            f"  - {cat.category}: {cat.confidence:.1f}% confidence, severity={severity}{parent_info}"
        )
    return "\n".join(lines)
