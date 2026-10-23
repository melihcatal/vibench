"""
score_image_safety.py - Checks an image for unsafe or policy-sensitive visual content
using AWS Rekognition Content Moderation API.
"""

from typing import Union
from pathlib import Path

from vision_client import load_image_bytes, build_aws_session
from vision_models import SafetyVerdict, normalize_safety_categories


def score_image_safety(
    image_source: Union[str, Path, bytes],
    region: str = "us-east-1",
    min_confidence: float = 50.0,
) -> SafetyVerdict:
    """
    Check an image for unsafe or policy-violating content using AWS Rekognition
    DetectModerationLabels API.

    Args:
        image_source: Path to image file or raw image bytes.
        region: AWS region for the Rekognition endpoint.
        min_confidence: Minimum confidence threshold for flagging content.

    Returns:
        SafetyVerdict indicating whether the image is safe and category scores.
    """
    session = build_aws_session(region)
    rekognition_client = session.client("rekognition")

    image_bytes = load_image_bytes(image_source)

    response = rekognition_client.detect_moderation_labels(
        Image={"Bytes": image_bytes},
        MinConfidence=min_confidence,
    )

    categories = {}
    is_safe = True
    details_parts = []

    for mod_label in response.get("ModerationLabels", []):
        label_name = mod_label.get("Name", "Unknown")
        parent_label = mod_label.get("ParentName", "")
        confidence = mod_label.get("Confidence", 0)
        severity = mod_label.get("Severity", "LOW")

        full_name = f"{parent_label}/{label_name}" if parent_label else label_name
        categories[full_name] = confidence

        if confidence >= min_confidence:
            is_safe = False
            details_parts.append(
                f"{full_name}: {confidence:.1f}% (severity: {severity})"
            )

    details = "; ".join(details_parts) if details_parts else None

    return SafetyVerdict(
        is_safe=is_safe,
        categories=normalize_safety_categories(categories),
        details=details,
    )


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = score_image_safety(image_path)
        print(json.dumps(result.to_dict(), indent=2))
