from __future__ import annotations

from vision_client import image_location, load_image_bytes, rekognition_client
from vision_models import ImageInput, TextDetectionResult, normalize_rekognition_text


def detect_image_text(image: ImageInput | str) -> dict:
    normalized = image_location(image)
    client = rekognition_client()
    response = client.detect_text(Image={"Bytes": load_image_bytes(normalized)})
    text, blocks = normalize_rekognition_text(response)
    result = TextDetectionResult(
        provider="amazon-rekognition",
        text=text,
        blocks=blocks,
        raw_response=response,
    )
    return result.to_dict()
