import os
import boto3
from typing import List, Dict, Any


def detect_image_text(image_path: str) -> List[Dict[str, Any]]:
    """
    Detects text appearing inside an image using AWS Rekognition.

    Args:
        image_path: Path to the image file

    Returns:
        List of detected text items with bounding boxes and confidence scores
    """
    client = boto3.client("rekognition")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={"Bytes": image_bytes})

    text_detections = response.get("TextDetections", [])

    results = []
    for detection in text_detections:
        if detection["Type"] == "LINE":
            results.append(
                {
                    "text": detection["DetectedText"],
                    "confidence": detection["Confidence"],
                    "bounding_box": detection.get("Geometry", {}).get(
                        "BoundingBox", {}
                    ),
                    "type": detection["Type"],
                }
            )

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python detect_image_text.py <image_path>")
        sys.exit(1)

    try:
        text_items = detect_image_text(sys.argv[1])
        for item in text_items:
            print(f"Text: {item['text']} (Confidence: {item['confidence']:.2f}%)")
    except Exception as e:
        print(f"Error: {e}")
