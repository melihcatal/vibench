"""
detect_image_labels.py - Detects labels or objects in a static image
using AWS Rekognition DetectLabels API.

Provider: AWS Rekognition (boto3 SDK)
API hostname: https://rekognition.{region}.amazonaws.com
"""

import os
import sys
from typing import List, Optional

from vision_client import (
    get_rekognition_client,
    load_image_as_bytes,
    prepare_rekognition_image_payload,
    validate_image_size,
)
from vision_models import (
    LabelDetectionRequest,
    LabelDetectionResponse,
    DetectedLabel,
    normalize_rekognition_labels,
)

AWS_REKOGNITION_SERVICE = "rekognition"
REKOGNITION_DETECT_LABELS_ACTION = "rekognition:DetectLabels"


def detect_labels(
    image_path: str,
    min_confidence: float = 50.0,
    max_labels: int = 50,
) -> LabelDetectionResponse:
    """
    Detect labels and objects in a static image using AWS Rekognition.

    Uses the Rekognition DetectLabels API to identify objects, scenes,
    and concepts in the image with confidence scores.

    Args:
        image_path: Path to the local image file.
        min_confidence: Minimum confidence threshold (0.0-100.0).
        max_labels: Maximum number of labels to return.

    Returns:
        LabelDetectionResponse containing detected labels.
    """
    image_bytes = load_image_as_bytes(image_path)

    if not validate_image_size(image_bytes):
        raise ValueError(
            f"Image exceeds 5MB size limit for AWS Rekognition: {len(image_bytes)} bytes"
        )

    client = get_rekognition_client()
    rekognition_payload = prepare_rekognition_image_payload(image_bytes)

    response = client.detect_labels(
        Image=rekognition_payload,
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    labels = normalize_rekognition_labels(response, min_confidence)

    return LabelDetectionResponse(
        labels=labels,
        raw_response=response,
    )


def detect_labels_from_bytes(
    image_bytes: bytes,
    min_confidence: float = 50.0,
    max_labels: int = 50,
) -> LabelDetectionResponse:
    """
    Detect labels and objects from raw image bytes using AWS Rekognition.

    Args:
        image_bytes: Raw bytes of the image.
        min_confidence: Minimum confidence threshold (0.0-100.0).
        max_labels: Maximum number of labels to return.

    Returns:
        LabelDetectionResponse containing detected labels.
    """
    if not validate_image_size(image_bytes):
        raise ValueError(
            f"Image exceeds 5MB size limit for AWS Rekognition: {len(image_bytes)} bytes"
        )

    client = get_rekognition_client()
    rekognition_payload = prepare_rekognition_image_payload(image_bytes)

    response = client.detect_labels(
        Image=rekognition_payload,
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    labels = normalize_rekognition_labels(response, min_confidence)

    return LabelDetectionResponse(
        labels=labels,
        raw_response=response,
    )


def print_label_results(response: LabelDetectionResponse) -> None:
    """Print detected labels in a human-readable format."""
    print(f"Detected {len(response.labels)} labels:")
    for label in sorted(response.labels, key=lambda l: l.confidence, reverse=True):
        parents_str = f" (parents: {', '.join(label.parents)})" if label.parents else ""
        print(f"  - {label.name}: {label.confidence:.1f}%{parents_str}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_image_labels.py <image_path> [min_confidence] [max_labels]")
        sys.exit(1)

    image_file = sys.argv[1]
    confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0
    max_lbls = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    result = detect_labels(image_file, min_confidence=confidence, max_labels=max_lbls)
    print_label_results(result)
