from __future__ import annotations

from vision_client import create_rekognition_client, load_image_bytes
from vision_models import (
    ImageInput,
    SafetyScoreResult,
    normalize_rekognition_moderation,
)


def score_image_safety(image: ImageInput, threshold: float = 60.0) -> dict:
    client = create_rekognition_client()
    response = client.detect_moderation_labels(Image={"Bytes": load_image_bytes(image)})
    normalized = normalize_rekognition_moderation(response, threshold)
    return SafetyScoreResult(
        provider="amazon-rekognition",
        safe=normalized["safe"],
        scores=normalized["scores"],
        flagged_categories=normalized["flagged_categories"],
    ).to_dict()
