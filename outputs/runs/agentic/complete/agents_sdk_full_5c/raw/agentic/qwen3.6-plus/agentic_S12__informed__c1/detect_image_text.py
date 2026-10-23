"""
detect_image_text.py - Detects text appearing inside an image
using Amazon Rekognition Text Detection.

Provider: Amazon Rekognition
SDK: boto3 (service: rekognition)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import sys
from typing import Optional, List

from vision_client import get_rekognition_client, get_rekognition_image_payload
from vision_models import ImageTextResult, DetectedTextRegion


def detect_text_in_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> ImageTextResult:
    """
    Detect all text regions (words and lines) in a static image
    using Amazon Rekognition Text Detection.

    Args:
        image_path: Path to the image file on disk.
        image_bytes: Raw image bytes as an alternative.

    Returns:
        ImageTextResult containing detected text regions and metadata.
    """
    client = get_rekognition_client()
    image_payload = get_rekognition_image_payload(
        image_path=image_path, image_bytes=image_bytes
    )

    response = client.detect_text(
        Image=image_payload,
    )

    return ImageTextResult.from_rekognition_response(response)


def extract_text_blocks(
    result: ImageTextResult,
    min_confidence: float = 70.0,
    include_words: bool = False,
) -> List[str]:
    """
    Extract readable text blocks from detection results.

    Args:
        result: The ImageTextResult from detect_text_in_image.
        min_confidence: Minimum confidence threshold.
        include_words: If True, include individual WORD detections; otherwise only LINEs.

    Returns:
        List of detected text strings.
    """
    blocks = []
    for td in result.text_detections:
        if td.confidence < min_confidence:
            continue
        if include_words or td.label_type == "LINE":
            blocks.append(td.detected_text)
    return blocks


def get_text_with_locations(
    result: ImageTextResult,
    min_confidence: float = 70.0,
) -> List[dict]:
    """
    Return detected text with bounding box locations.

    Returns a list of dicts with keys: text, confidence, bbox.
    """
    located_texts = []
    for td in result.text_detections:
        if td.confidence < min_confidence:
            continue
        located_texts.append({
            "text": td.detected_text,
            "confidence": round(td.confidence, 2),
            "type": td.label_type,
            "bbox": td.bounding_box,
        })
    return located_texts


def main():
    """CLI entry point for text detection."""
    if len(sys.argv) < 2:
        print("Usage: python detect_image_text.py <image_path> [min_confidence]")
        sys.exit(1)

    image_path = sys.argv[1]
    min_confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 70.0

    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    result = detect_text_in_image(image_path=image_path)
    text_lines = extract_text_blocks(result, min_confidence=min_confidence, include_words=False)

    print(f"Text model version: {result.text_model_version}")
    print(f"Detected {len(text_lines)} text lines (confidence >= {min_confidence}%):")
    for i, text in enumerate(text_lines, 1):
        print(f"  {i}. {text}")


if __name__ == "__main__":
    main()
