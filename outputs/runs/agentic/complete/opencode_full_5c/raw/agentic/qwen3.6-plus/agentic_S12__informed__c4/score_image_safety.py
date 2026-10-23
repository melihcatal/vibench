import os
from typing import Optional

from vision_client import (
    get_rekognition_client,
    build_rekognition_image_payload,
    encode_image_to_bytes,
    encode_image_from_url,
)
from vision_models import (
    ImageAnalysisRequest,
    SafetyScoreResponse,
    normalize_moderation,
)


MODERATION_THRESHOLD = float(os.environ.get("REKOGNITION_MODERATION_THRESHOLD", "0.5"))


def score_image_safety(
    request: ImageAnalysisRequest, threshold: float = MODERATION_THRESHOLD
) -> SafetyScoreResponse:
    client = get_rekognition_client()

    if request.image_bytes:
        image_bytes = request.image_bytes
    elif request.image_url:
        image_bytes, _ = encode_image_from_url(request.image_url)
    else:
        raise ValueError("Either image_url or image_bytes must be provided")

    image_payload = build_rekognition_image_payload(image_bytes)

    response = client.detect_moderation_labels(
        Image=image_payload,
        MinConfidence=threshold * 100,
    )

    raw_labels = response.get("ModerationLabels", [])
    safety_response = normalize_moderation(raw_labels, threshold=threshold)
    safety_response.model = "amazon-rekognition"

    return safety_response


def score_safety_from_file(
    image_path: str, threshold: float = MODERATION_THRESHOLD
) -> SafetyScoreResponse:
    image_bytes, fmt = encode_image_to_bytes(image_path)
    request = ImageAnalysisRequest(image_bytes=image_bytes, image_format=fmt)
    return score_image_safety(request, threshold=threshold)


def score_safety_from_url(
    image_url: str, threshold: float = MODERATION_THRESHOLD
) -> SafetyScoreResponse:
    image_bytes, fmt = encode_image_from_url(image_url)
    request = ImageAnalysisRequest(
        image_url=image_url, image_bytes=image_bytes, image_format=fmt
    )
    return score_image_safety(request, threshold=threshold)
