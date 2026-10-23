"""
detect_image_text.py - Detects text appearing inside an image
using AWS Rekognition Text Detection API.
"""

from typing import List, Union
from pathlib import Path

from vision_client import load_image_bytes, build_aws_session
from vision_models import DetectedText, normalize_text_detections


def detect_image_text(
    image_source: Union[str, Path, bytes],
    region: str = "us-east-1",
) -> List[DetectedText]:
    """
    Detect and extract text from an image using AWS Rekognition DetectText.

    Args:
        image_source: Path to image file or raw image bytes.
        region: AWS region for the Rekognition endpoint.

    Returns:
        List of DetectedText objects with extracted text and confidence.
    """
    session = build_aws_session(region)
    rekognition_client = session.client("rekognition")

    image_bytes = load_image_bytes(image_source)

    response = rekognition_client.detect_text(
        Image={"Bytes": image_bytes},
    )

    raw_items = []
    for text_detection in response.get("TextDetections", []):
        if text_detection.get("Type") == "LINE":
            item = {
                "text": text_detection.get("DetectedText", ""),
                "confidence": text_detection.get("Confidence", 0),
            }
            bounding_box = text_detection.get("Geometry", {}).get("BoundingBox", {})
            if bounding_box:
                item["bounding_box"] = [
                    bounding_box.get("Left", 0),
                    bounding_box.get("Top", 0),
                    bounding_box.get("Width", 0),
                    bounding_box.get("Height", 0),
                ]
            raw_items.append(item)

    return normalize_text_detections(raw_items)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        results = detect_image_text(image_path)
        for dt in results:
            print(f'"{dt.text}" (confidence: {dt.confidence:.2f})')
