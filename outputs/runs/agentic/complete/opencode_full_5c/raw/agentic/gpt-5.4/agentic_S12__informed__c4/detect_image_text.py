from __future__ import annotations

from vision_client import create_rekognition_client, load_image_bytes
from vision_models import ImageInput, TextDetectionResult, normalize_rekognition_text


def detect_image_text(image: ImageInput) -> dict:
    client = create_rekognition_client()
    response = client.detect_text(Image={"Bytes": load_image_bytes(image)})
    text, blocks = normalize_rekognition_text(response)
    return TextDetectionResult(
        provider="amazon-rekognition",
        text=text,
        blocks=blocks,
    ).to_dict()
