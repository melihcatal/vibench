"""
score_image_safety.py - Checks an image for unsafe or policy-sensitive
visual content using Amazon Rekognition Content Moderation.

Provider: Amazon Rekognition
SDK: boto3 (service: rekognition)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import sys
from typing import Optional, List, Dict, Any

from vision_client import get_rekognition_client, get_rekognition_image_payload
from vision_models import ImageSafetyResult, SafetyFinding, compute_safety_score


def check_image_safety(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    min_confidence: float = 50.0,
) -> ImageSafetyResult:
    """
    Analyze an image for unsafe or policy-sensitive visual content
    using Amazon Rekognition Content Moderation.

    Args:
        image_path: Path to the image file on disk.
        image_bytes: Raw image bytes as an alternative.
        min_confidence: Minimum confidence threshold for moderation labels.

    Returns:
        ImageSafetyResult containing moderation findings and metadata.
    """
    client = get_rekognition_client()
    image_payload = get_rekognition_image_payload(
        image_path=image_path, image_bytes=image_bytes
    )

    response = client.detect_moderation_labels(
        Image=image_payload,
        MinConfidence=min_confidence,
    )

    return ImageSafetyResult.from_rekognition_response(response)


def get_safety_assessment(
    result: ImageSafetyResult,
) -> Dict[str, Any]:
    """
    Produce a structured safety assessment from moderation results.

    Returns a dict with:
    - is_safe: boolean indicating if image passes safety checks
    - safety_score: float from 0.0 (unsafe) to 1.0 (safe)
    - flagged_labels: list of concerning labels
    - highest_confidence_violation: highest confidence moderation label
    """
    safety_score = compute_safety_score(result)
    is_safe = safety_score >= 0.85

    flagged_labels = [
        {
            "name": finding.name,
            "confidence": round(finding.confidence, 2),
        }
        for finding in result.moderation_labels
    ]

    highest_confidence_violation = None
    if result.moderation_labels:
        top = max(result.moderation_labels, key=lambda f: f.confidence)
        highest_confidence_violation = {
            "name": top.name,
            "confidence": round(top.confidence, 2),
        }

    return {
        "is_safe": is_safe,
        "safety_score": safety_score,
        "flagged_labels": flagged_labels,
        "highest_confidence_violation": highest_confidence_violation,
        "model_version": result.moderation_model_version,
    }


def format_safety_report(assessment: Dict[str, Any]) -> str:
    """Format the safety assessment into a human-readable report."""
    lines = []
    lines.append(f"Safety Assessment Report")
    lines.append(f"{'=' * 40}")
    lines.append(f"Overall safe: {assessment['is_safe']}")
    lines.append(f"Safety score: {assessment['safety_score']}")
    lines.append(f"Moderation model: {assessment['model_version']}")

    if assessment["flagged_labels"]:
        lines.append(f"\nFlagged content ({len(assessment['flagged_labels'])} findings):")
        for label in assessment["flagged_labels"]:
            lines.append(f"  - {label['name']} (confidence: {label['confidence']}%)")
    else:
        lines.append("\nNo policy-sensitive content detected.")

    if assessment["highest_confidence_violation"]:
        top = assessment["highest_confidence_violation"]
        lines.append(f"\nHighest confidence concern: {top['name']} at {top['confidence']}%")

    return "\n".join(lines)


def main():
    """CLI entry point for image safety scoring."""
    if len(sys.argv) < 2:
        print("Usage: python score_image_safety.py <image_path> [min_confidence]")
        sys.exit(1)

    image_path = sys.argv[1]
    min_confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0

    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    result = check_image_safety(image_path=image_path, min_confidence=min_confidence)
    assessment = get_safety_assessment(result)
    report = format_safety_report(assessment)

    print(report)


if __name__ == "__main__":
    main()
