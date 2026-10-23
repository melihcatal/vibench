import os
from typing import List, Optional

from vision_client import (
    get_rekognition_client,
    build_rekognition_image_payload,
    encode_image_to_bytes,
    encode_image_from_url,
)
from vision_models import (
    ImageAnalysisRequest,
    TextDetectionResponse,
    DetectedText,
    normalize_text_detections,
)


TEXT_CONFIDENCE_THRESHOLD = float(os.environ.get("REKOGNITION_TEXT_CONFIDENCE", "50.0"))


def detect_image_text(
    request: ImageAnalysisRequest,
    confidence_threshold: float = TEXT_CONFIDENCE_THRESHOLD,
) -> TextDetectionResponse:
    client = get_rekognition_client()

    if request.image_bytes:
        image_bytes = request.image_bytes
    elif request.image_url:
        image_bytes, _ = encode_image_from_url(request.image_url)
    else:
        raise ValueError("Either image_url or image_bytes must be provided")

    image_payload = build_rekognition_image_payload(image_bytes)

    response = client.detect_text(Image=image_payload)

    raw_detections = response.get("TextDetections", [])
    detected_texts = normalize_text_detections(
        raw_detections, confidence_threshold=confidence_threshold
    )

    full_text = " ".join(dt.text for dt in detected_texts)

    return TextDetectionResponse(
        detected_texts=detected_texts,
        full_text=full_text,
        model="amazon-rekognition",
    )


def detect_text_from_file(
    image_path: str, confidence_threshold: float = TEXT_CONFIDENCE_THRESHOLD
) -> TextDetectionResponse:
    image_bytes, fmt = encode_image_to_bytes(image_path)
    request = ImageAnalysisRequest(image_bytes=image_bytes, image_format=fmt)
    return detect_image_text(request, confidence_threshold=confidence_threshold)


def detect_text_from_url(
    image_url: str, confidence_threshold: float = TEXT_CONFIDENCE_THRESHOLD
) -> TextDetectionResponse:
    image_bytes, fmt = encode_image_from_url(image_url)
    request = ImageAnalysisRequest(
        image_url=image_url, image_bytes=image_bytes, image_format=fmt
    )
    return detect_image_text(request, confidence_threshold=confidence_threshold)
