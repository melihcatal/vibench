from __future__ import annotations

from vision_client import image_location, load_image_bytes, rekognition_client
from vision_models import ImageInput, LabelDetectionResult, normalize_rekognition_labels


def detect_image_labels(
    image: ImageInput | str, max_labels: int = 15, min_confidence: float = 70.0
) -> dict:
    normalized = image_location(image)
    client = rekognition_client()
    response = client.detect_labels(
        Image={"Bytes": load_image_bytes(normalized)},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
        Features=["GENERAL_LABELS"],
    )
    result = LabelDetectionResult(
        provider="amazon-rekognition",
        labels=normalize_rekognition_labels(response),
        raw_response=response,
    )
    return result.to_dict()
