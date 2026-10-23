from __future__ import annotations

from vision_client import create_rekognition_client, load_image_bytes
from vision_models import ImageInput, LabelDetectionResult, normalize_rekognition_labels


def detect_image_labels(
    image: ImageInput, max_labels: int = 20, min_confidence: float = 70.0
) -> dict:
    client = create_rekognition_client()
    response = client.detect_labels(
        Image={"Bytes": load_image_bytes(image)},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )
    return LabelDetectionResult(
        provider="amazon-rekognition",
        labels=normalize_rekognition_labels(response),
    ).to_dict()
