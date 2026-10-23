"""
score_image_safety.py - Checks an image for unsafe or policy-sensitive visual content
using AWS Rekognition DetectModerationLabels API.

Provider: AWS Rekognition (boto3 SDK)
API hostname: https://rekognition.{region}.amazonaws.com
"""

import sys
from typing import List, Optional

from vision_client import (
    get_rekognition_client,
    load_image_as_bytes,
    prepare_rekognition_image_payload,
    validate_image_size,
)
from vision_models import (
    ImageSafetyRequest,
    ImageSafetyResponse,
    SafetyFinding,
    normalize_rekognition_moderation,
)

AWS_REKOGNITION_SERVICE = "rekognition"
REKOGNITION_DETECT_MODERATION_ACTION = "rekognition:DetectModerationLabels"

POLICY_SENSITIVE_CATEGORIES = {
    "Explicit Nudity",
    "Suggestive",
    "Violence",
    "Visually Disturbing",
    "Hate Symbols",
    "Drugs",
    "Tobacco",
    "Alcohol",
    "Gambling",
    "Weapons",
}


def score_image_safety(
    image_path: str,
    min_confidence: float = 50.0,
) -> ImageSafetyResponse:
    """
    Check a static image for unsafe or policy-sensitive visual content using AWS Rekognition.

    Uses the DetectModerationLabels API to identify potentially unsafe content
    categories such as violence, explicit content, and hate symbols.

    Args:
        image_path: Path to the local image file.
        min_confidence: Minimum confidence threshold (0.0-100.0).

    Returns:
        ImageSafetyResponse with safety findings and overall safety verdict.
    """
    image_bytes = load_image_as_bytes(image_path)

    if not validate_image_size(image_bytes):
        raise ValueError(
            f"Image exceeds 5MB size limit for AWS Rekognition: {len(image_bytes)} bytes"
        )

    client = get_rekognition_client()
    rekognition_payload = prepare_rekognition_image_payload(image_bytes)

    response = client.detect_moderation_labels(
        Image=rekognition_payload,
        MinConfidence=min_confidence,
    )

    findings = normalize_rekognition_moderation(response, min_confidence)

    is_safe = not any(
        f.category in POLICY_SENSITIVE_CATEGORIES for f in findings
    )

    return ImageSafetyResponse(
        is_safe=is_safe,
        findings=findings,
        raw_response=response,
    )


def score_image_safety_from_bytes(
    image_bytes: bytes,
    min_confidence: float = 50.0,
) -> ImageSafetyResponse:
    """
    Check raw image bytes for unsafe or policy-sensitive visual content using AWS Rekognition.

    Args:
        image_bytes: Raw bytes of the image.
        min_confidence: Minimum confidence threshold (0.0-100.0).

    Returns:
        ImageSafetyResponse with safety findings and overall safety verdict.
    """
    if not validate_image_size(image_bytes):
        raise ValueError(
            f"Image exceeds 5MB size limit for AWS Rekognition: {len(image_bytes)} bytes"
        )

    client = get_rekognition_client()
    rekognition_payload = prepare_rekognition_image_payload(image_bytes)

    response = client.detect_moderation_labels(
        Image=rekognition_payload,
        MinConfidence=min_confidence,
    )

    findings = normalize_rekognition_moderation(response, min_confidence)

    is_safe = not any(
        f.category in POLICY_SENSITIVE_CATEGORIES for f in findings
    )

    return ImageSafetyResponse(
        is_safe=is_safe,
        findings=findings,
        raw_response=response,
    )


def get_safety_score(response: ImageSafetyResponse) -> float:
    """
    Calculate a numerical safety score (0.0 = unsafe, 1.0 = fully safe).

    Args:
        response: ImageSafetyResponse from score_image_safety.

    Returns:
        Safety score between 0.0 and 1.0.
    """
    if not response.findings:
        return 1.0

    max_confidence = max(f.confidence for f in response.findings) / 100.0
    return max(0.0, 1.0 - max_confidence)


def print_safety_results(response: ImageSafetyResponse) -> None:
    """Print safety analysis results in a human-readable format."""
    safety_score = get_safety_score(response)
    status = "SAFE" if response.is_safe else "UNSAFE / POLICY SENSITIVE"
    print(f"Image Safety: {status} (score: {safety_score:.2f})")

    if response.findings:
        print("\nModeration findings:")
        for finding in sorted(response.findings, key=lambda f: f.confidence, reverse=True):
            parent_info = f" (parent: {finding.parent_name})" if finding.parent_name else ""
            print(f"  - {finding.category}: {finding.confidence:.1f}%{parent_info}")
    else:
        print("\nNo moderation concerns detected.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python score_image_safety.py <image_path> [min_confidence]")
        sys.exit(1)

    image_file = sys.argv[1]
    confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0

    result = score_image_safety(image_file, min_confidence=confidence)
    print_safety_results(result)
