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
    LabelDetectionResponse,
    DetectedLabel,
    normalize_labels,
)


CONFIDENCE_THRESHOLD = float(os.environ.get("REKOGNITION_LABEL_CONFIDENCE", "50.0"))


def detect_image_labels(
    request: ImageAnalysisRequest, confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> LabelDetectionResponse:
    client = get_rekognition_client()

    if request.image_bytes:
        image_bytes = request.image_bytes
    elif request.image_url:
        image_bytes, _ = encode_image_from_url(request.image_url)
    else:
        raise ValueError("Either image_url or image_bytes must be provided")

    image_payload = build_rekognition_image_payload(image_bytes)

    kwargs = {
        "Image": image_payload,
        "MaxLabels": 50,
        "MinConfidence": confidence_threshold,
    }

    response = client.detect_labels(**kwargs)

    raw_labels = response.get("Labels", [])
    labels = normalize_labels(raw_labels, confidence_threshold=0.0)

    image_meta = response.get("ImageMetadata", {})

    return LabelDetectionResponse(
        labels=labels,
        image_width=image_meta.get("Width", 0),
        image_height=image_meta.get("Height", 0),
        model="amazon-rekognition",
    )


def detect_labels_from_file(
    image_path: str, confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> LabelDetectionResponse:
    image_bytes, fmt = encode_image_to_bytes(image_path)
    request = ImageAnalysisRequest(image_bytes=image_bytes, image_format=fmt)
    return detect_image_labels(request, confidence_threshold=confidence_threshold)


def detect_labels_from_url(
    image_url: str, confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> LabelDetectionResponse:
    image_bytes, fmt = encode_image_from_url(image_url)
    request = ImageAnalysisRequest(
        image_url=image_url, image_bytes=image_bytes, image_format=fmt
    )
    return detect_image_labels(request, confidence_threshold=confidence_threshold)
