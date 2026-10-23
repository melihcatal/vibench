from __future__ import annotations

from vision_client import get_aws_rekognition_client
from vision_models import ImageSource, LabelDetectionResult, normalize_labels


def detect_image_labels(
    image: ImageSource, max_labels: int = 10, min_confidence: float = 70.0
) -> LabelDetectionResult:
    client = get_aws_rekognition_client()
    if not image.image_bytes:
        raise ValueError("AWS Rekognition DetectLabels requires image_bytes")
    response = client.detect_labels(
        Image={"Bytes": image.image_bytes},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )
    labels = normalize_labels(
        [item["Name"] for item in response.get("Labels", [])], limit=max_labels
    )
    return LabelDetectionResult(
        provider="aws_rekognition", labels=labels, raw_response=response
    )
