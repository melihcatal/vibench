from __future__ import annotations

from vision_client import get_aws_rekognition_client
from vision_models import ImageSource, SafetyScoreResult


def score_image_safety(image: ImageSource) -> SafetyScoreResult:
    client = get_aws_rekognition_client()
    if not image.image_bytes:
        raise ValueError("AWS Rekognition DetectModerationLabels requires image_bytes")
    response = client.detect_moderation_labels(
        Image={"Bytes": image.image_bytes}, MinConfidence=50
    )
    category_scores = {}
    for label in response.get("ModerationLabels", []):
        category_scores[label["Name"]] = float(label.get("Confidence", 0.0))
    return SafetyScoreResult(
        provider="aws_rekognition",
        safe=not bool(category_scores),
        categories=category_scores,
        raw_response=response,
    )
