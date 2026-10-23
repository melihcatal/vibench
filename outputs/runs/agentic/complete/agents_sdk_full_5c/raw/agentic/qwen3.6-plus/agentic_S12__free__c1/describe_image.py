"""
describe_image.py - Generates a short visual description for an image
using AWS Rekognition DetectLabels API.

Provider: AWS Rekognition (boto3 SDK)
API hostname: https://rekognition.{region}.amazonaws.com
"""

import sys
from typing import Optional

from vision_client import (
    get_rekognition_client,
    load_image_as_bytes,
    prepare_rekognition_image_payload,
    validate_image_size,
)
from vision_models import (
    ImageDescriptionRequest,
    ImageDescriptionResponse,
    normalize_rekognition_labels,
    build_description_from_labels,
)

AWS_REKOGNITION_SERVICE = "rekognition"
REKOGNITION_DETECT_LABELS_ACTION = "rekognition:DetectLabels"


def describe_image(
    image_path: str,
    min_confidence: float = 50.0,
    max_labels: int = 10,
    max_description_length: int = 500,
) -> ImageDescriptionResponse:
    """
    Generate a short visual description for a static image using AWS Rekognition.

    Leages the Rekognition DetectLabels API to identify key objects and
    scenes, then synthesizes a natural-language description from those labels.

    Args:
        image_path: Path to the local image file.
        min_confidence: Minimum confidence threshold for label detection.
        max_labels: Maximum labels to consider for description.
        max_description_length: Maximum length of the generated description.

    Returns:
        ImageDescriptionResponse with a human-readable description.
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
    description = build_description_from_labels(labels, max_length=max_description_length)
    label_names = [l.name for l in labels]

    return ImageDescriptionResponse(
        description=description,
        labels_used=label_names,
        raw_response=response,
    )


def describe_image_from_bytes(
    image_bytes: bytes,
    min_confidence: float = 50.0,
    max_labels: int = 10,
    max_description_length: int = 500,
) -> ImageDescriptionResponse:
    """
    Generate a short visual description from raw image bytes using AWS Rekognition.

    Args:
        image_bytes: Raw bytes of the image.
        min_confidence: Minimum confidence threshold for label detection.
        max_labels: Maximum labels to consider for description.
        max_description_length: Maximum length of the generated description.

    Returns:
        ImageDescriptionResponse with a human-readable description.
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
    description = build_description_from_labels(labels, max_length=max_description_length)
    label_names = [l.name for l in labels]

    return ImageDescriptionResponse(
        description=description,
        labels_used=label_names,
        raw_response=response,
    )


def print_description(result: ImageDescriptionResponse) -> None:
    """Print the image description and supporting labels."""
    print(f"Image Description:\n  {result.description}")
    if result.labels_used:
        print(f"\nSupporting labels: {', '.join(result.labels_used)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python describe_image.py <image_path> [min_confidence]")
        sys.exit(1)

    image_file = sys.argv[1]
    confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0

    result = describe_image(image_file, min_confidence=confidence)
    print_description(result)
