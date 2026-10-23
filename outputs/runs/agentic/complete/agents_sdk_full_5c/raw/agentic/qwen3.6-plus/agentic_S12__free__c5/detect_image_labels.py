"""
detect_image_labels.py - Detects labels or objects in a static image
using AWS Rekognition.
"""

from typing import List, Union
from pathlib import Path

from vision_client import load_image_bytes, build_aws_session
from vision_models import ImageLabel, normalize_label_confidence


def detect_image_labels(
    image_source: Union[str, Path, bytes],
    region: str = "us-east-1",
    max_labels: int = 10,
    min_confidence: float = 50.0,
) -> List[ImageLabel]:
    """
    Detect labels/objects in an image using AWS Rekognition DetectLabels API.

    Args:
        image_source: Path to image file or raw image bytes.
        region: AWS region for the Rekognition endpoint.
        max_labels: Maximum number of labels to return.
        min_confidence: Minimum confidence threshold (0-100).

    Returns:
        List of ImageLabel objects sorted by descending confidence.
    """
    session = build_aws_session(region)
    rekognition_client = session.client("rekognition")

    image_bytes = load_image_bytes(image_source)

    response = rekognition_client.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    labels = []
    for label_entry in response.get("Labels", []):
        parent_names = [
            parent["Name"] for parent in label_entry.get("Parents", [])
        ]
        confidence = normalize_label_confidence(
            label_entry.get("Confidence", 0) / 100.0
        )
        labels.append(
            ImageLabel(
                name=label_entry["Name"],
                confidence=confidence,
                parent_names=parent_names,
            )
        )

    labels.sort(key=lambda l: l.confidence, reverse=True)
    return labels


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        results = detect_image_labels(image_path)
        for label in results:
            print(f"{label.name}: {label.confidence:.2f}")
