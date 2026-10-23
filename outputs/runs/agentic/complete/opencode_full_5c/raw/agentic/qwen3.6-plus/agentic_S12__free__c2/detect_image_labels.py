import os
import base64
from typing import List, Dict, Optional
import boto3
from botocore.config import Config

from vision_client import get_rekognition_client, load_image_bytes
from vision_models import ImageLabelRequest, ImageLabelResponse, normalize_label


def detect_image_labels(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_labels: int = 10,
    min_confidence: float = 50.0,
) -> ImageLabelResponse:
    if image_path is None and image_bytes is None:
        raise ValueError("Either image_path or image_bytes must be provided")

    if image_bytes is None:
        image_bytes = load_image_bytes(image_path)

    client = get_rekognition_client()

    payload: Dict = {
        "Image": {"Bytes": image_bytes},
        "MaxLabels": max_labels,
        "MinConfidence": min_confidence,
    }

    response = client.detect_labels(**payload)

    labels = []
    for label_data in response.get("Labels", []):
        normalized = normalize_label(
            name=label_data["Name"],
            confidence=label_data["Confidence"],
            instances=[
                {
                    "bounding_box": inst["BoundingBox"],
                    "confidence": inst["Confidence"],
                }
                for inst in label_data.get("Instances", [])
            ],
            parents=[p["Name"] for p in label_data.get("Parents", [])],
        )
        labels.append(normalized)

    return ImageLabelResponse(
        labels=labels,
        label_model="aws-rekognition-detect-labels-v3",
        orientation_correction=response.get("OrientationCorrection"),
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_image_labels.py <image_path>")
        sys.exit(1)

    result = detect_image_labels(image_path=sys.argv[1])
    for label in result.labels:
        print(f"{label.name}: {label.confidence:.1f}%")
