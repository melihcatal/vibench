"""
detect_image_labels.py - Detects labels or objects in a static image
using Amazon Rekognition.

Provider: Amazon Rekognition
SDK: boto3 (service: rekognition)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import sys
from typing import List, Dict, Any, Optional

from vision_client import get_rekognition_client, get_rekognition_image_payload
from vision_models import ImageLabelResult, normalize_label_list_for_summary


def detect_labels_in_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_labels: int = 20,
    min_confidence: float = 50.0,
) -> ImageLabelResult:
    """
    Detect labels/objects in a static image using Amazon Rekognition.

    Args:
        image_path: Path to the image file on disk.
        image_bytes: Raw image bytes as an alternative to image_path.
        max_labels: Maximum number of labels to return.
        min_confidence: Minimum confidence threshold for returned labels.

    Returns:
        ImageLabelResult containing detected labels and metadata.
    """
    client = get_rekognition_client()
    image_payload = get_rekognition_image_payload(
        image_path=image_path, image_bytes=image_bytes
    )

    response = client.detect_labels(
        Image=image_payload,
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    return ImageLabelResult.from_rekognition_response(response)


def format_label_summary(
    result: ImageLabelResult,
    min_confidence: float = 50.0,
    max_labels: int = 15,
) -> List[Dict[str, Any]]:
    """Format detected labels into a concise summary list."""
    return normalize_label_list_for_summary(
        result.labels, min_confidence=min_confidence, max_labels=max_labels
    )


def main():
    """CLI entry point for label detection."""
    if len(sys.argv) < 2:
        print("Usage: python detect_image_labels.py <image_path> [min_confidence]")
        sys.exit(1)

    image_path = sys.argv[1]
    min_confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0

    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    result = detect_labels_in_image(image_path=image_path, min_confidence=min_confidence)
    summary = format_label_summary(result, min_confidence=min_confidence)

    print(f"Model version: {result.label_model_version}")
    print(f"Detected {len(summary)} labels (confidence >= {min_confidence}%):")
    for label in summary:
        print(f"  - {label['name']}: {label['confidence']}%")


if __name__ == "__main__":
    main()
