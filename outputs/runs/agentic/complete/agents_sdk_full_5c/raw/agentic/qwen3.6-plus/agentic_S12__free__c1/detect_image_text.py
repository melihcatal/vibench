"""
detect_image_text.py - Detects text appearing inside an image
using AWS Rekognition DetectText API.

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
    TextDetectionRequest,
    TextDetectionResponse,
    DetectedText,
    normalize_rekognition_text,
)

AWS_REKOGNITION_SERVICE = "rekognition"
REKOGNITION_DETECT_TEXT_ACTION = "rekognition:DetectText"


def detect_text(
    image_path: str,
    min_confidence: float = 50.0,
) -> TextDetectionResponse:
    """
    Detect text appearing inside a static image using AWS Rekognition DetectText API.

    Identifies lines and words of text within the image, returning the detected
    text strings along with confidence scores and bounding box coordinates.

    Args:
        image_path: Path to the local image file.
        min_confidence: Minimum confidence threshold (0.0-100.0).

    Returns:
        TextDetectionResponse containing detected text lines.
    """
    image_bytes = load_image_as_bytes(image_path)

    if not validate_image_size(image_bytes):
        raise ValueError(
            f"Image exceeds 5MB size limit for AWS Rekognition: {len(image_bytes)} bytes"
        )

    client = get_rekognition_client()
    rekognition_payload = prepare_rekognition_image_payload(image_bytes)

    response = client.detect_text(
        Image=rekognition_payload,
    )

    detected_texts = normalize_rekognition_text(response, min_confidence)

    return TextDetectionResponse(
        detected_text=detected_texts,
        raw_response=response,
    )


def detect_text_from_bytes(
    image_bytes: bytes,
    min_confidence: float = 50.0,
) -> TextDetectionResponse:
    """
    Detect text from raw image bytes using AWS Rekognition DetectText API.

    Args:
        image_bytes: Raw bytes of the image.
        min_confidence: Minimum confidence threshold (0.0-100.0).

    Returns:
        TextDetectionResponse containing detected text lines.
    """
    if not validate_image_size(image_bytes):
        raise ValueError(
            f"Image exceeds 5MB size limit for AWS Rekognition: {len(image_bytes)} bytes"
        )

    client = get_rekognition_client()
    rekognition_payload = prepare_rekognition_image_payload(image_bytes)

    response = client.detect_text(
        Image=rekognition_payload,
    )

    detected_texts = normalize_rekognition_text(response, min_confidence)

    return TextDetectionResponse(
        detected_text=detected_texts,
        raw_response=response,
    )


def extract_text_strings(response: TextDetectionResponse) -> List[str]:
    """Extract plain text strings from a TextDetectionResponse."""
    return [t.text for t in response.detected_text]


def print_text_results(response: TextDetectionResponse) -> None:
    """Print detected text in a human-readable format."""
    print(f"Detected {len(response.detected_text)} text lines:")
    for i, text_item in enumerate(response.detected_text, 1):
        bbox_info = ""
        if text_item.bounding_box:
            bbox = text_item.bounding_box
            bbox_info = (
                f" [bbox: left={bbox.get('Left', 0):.3f}, "
                f"top={bbox.get('Top', 0):.3f}, "
                f"width={bbox.get('Width', 0):.3f}, "
                f"height={bbox.get('Height', 0):.3f}]"
            )
        print(f"  {i}. \"{text_item.text}\" ({text_item.confidence:.1f}%){bbox_info}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_image_text.py <image_path> [min_confidence]")
        sys.exit(1)

    image_file = sys.argv[1]
    confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0

    result = detect_text(image_file, min_confidence=confidence)
    print_text_results(result)
