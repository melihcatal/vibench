"""
describe_image.py - Generates a short visual description for an image
using Amazon Rekognition label and scene analysis.

Provider: Amazon Rekognition
SDK: boto3 (service: rekognition)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import sys
from typing import Optional, List, Dict, Any

from vision_client import get_rekognition_client, get_rekognition_image_payload
from vision_models import ImageLabelResult, ImageLabel


def detect_image_labels(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_labels: int = 20,
    min_confidence: float = 50.0,
) -> ImageLabelResult:
    """Call Amazon Rekognition to detect labels in the given image."""
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


def detect_image_scenes(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> List[Dict[str, Any]]:
    """
    Detect scene information using Amazon Rekognition's scene recognition.

    Returns a list of scene descriptions with confidence scores.
    """
    client = get_rekognition_client()
    image_payload = get_rekognition_image_payload(
        image_path=image_path, image_bytes=image_bytes
    )

    response = client.detect_labels(
        Image=image_payload,
        MaxLabels=10,
        MinConfidence=60.0,
    )

    scenes = []
    for label in response.get("Labels", []):
        for instance in label.get("Instances", []):
            scenes.append(
                {
                    "label": label["Name"],
                    "confidence": label.get("Confidence", 0.0),
                    "has_instance": True,
                }
            )
        if not label.get("Instances"):
            scenes.append(
                {
                    "label": label["Name"],
                    "confidence": label.get("Confidence", 0.0),
                    "has_instance": False,
                }
            )
    return scenes


def generate_visual_description(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> str:
    """
    Generate a short visual description for an image using
    Amazon Rekognition label analysis.

    Args:
        image_path: Path to the image file on disk.
        image_bytes: Raw image bytes as an alternative.

    Returns:
        A short descriptive string summarizing the image content.
    """
    label_result = detect_image_labels(
        image_path=image_path, image_bytes=image_bytes, max_labels=15
    )

    top_labels = sorted(
        label_result.labels, key=lambda x: x.confidence, reverse=True
    )[:8]

    if not top_labels:
        return "No recognizable content detected in the image."

    primary_labels = [lbl.name.lower() for lbl in top_labels[:3]]
    secondary_labels = [lbl.name.lower() for lbl in top_labels[3:]]

    confidences = {lbl.name: lbl.confidence for lbl in top_labels}

    primary_str = ", ".join(primary_labels)
    if secondary_labels:
        secondary_str = ", ".join(secondary_labels)
        description = (
            f"The image shows {primary_str} with average confidence "
            f"{sum(confidences[lbl] for lbl in primary_labels) / len(primary_labels):.1f}%. "
            f"Additional elements include {secondary_str}."
        )
    else:
        description = (
            f"The image primarily shows {primary_str} with an average confidence "
            f"of {sum(confidences[lbl] for lbl in primary_labels) / len(primary_labels):.1f}%."
        )

    return description


def main():
    """CLI entry point for image description."""
    if len(sys.argv) < 2:
        print("Usage: python describe_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    description = generate_visual_description(image_path=image_path)
    print(description)


if __name__ == "__main__":
    main()
