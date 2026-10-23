from __future__ import annotations

from vision_client import image_location, load_image_bytes, rekognition_client
from vision_models import ImageInput, normalize_rekognition_safety


def score_image_safety(
    image: ImageInput | str, confidence_threshold: float = 60.0
) -> dict:
    normalized = image_location(image)
    client = rekognition_client()
    response = client.detect_moderation_labels(
        Image={"Bytes": load_image_bytes(normalized)}
    )
    result = normalize_rekognition_safety(response, threshold=confidence_threshold)
    return result.to_dict()
