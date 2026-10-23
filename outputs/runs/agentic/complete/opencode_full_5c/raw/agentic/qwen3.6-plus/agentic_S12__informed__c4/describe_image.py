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
    ImageDescriptionResponse,
    LabelDetectionResponse,
    normalize_labels,
)
from detect_image_labels import detect_image_labels


CONFIDENCE_THRESHOLD = float(
    os.environ.get("REKOGNITION_DESCRIPTION_CONFIDENCE", "60.0")
)


def generate_description_from_labels(labels_response: LabelDetectionResponse) -> str:
    top_labels = sorted(
        labels_response.labels, key=lambda l: l.confidence, reverse=True
    )[:8]
    if not top_labels:
        return "No recognizable content in the image."

    label_names = [
        l.name.lower()
        for l in top_labels
        if l.name.lower() not in ("person", "people", "human")
    ]
    has_person = any(
        l.name.lower() in ("person", "people", "human") for l in top_labels
    )

    if label_names:
        subject = ", ".join(label_names[:4])
        if has_person:
            desc = f"The image shows a person with {subject}."
        else:
            desc = f"The image shows {subject}."
    elif has_person:
        desc = "The image shows a person."
    else:
        desc = "The image contains visual content."

    return desc


def describe_image(
    request: ImageAnalysisRequest, confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> ImageDescriptionResponse:
    labels_response = detect_image_labels(
        request, confidence_threshold=confidence_threshold
    )

    description = generate_description_from_labels(labels_response)

    tags = [l.name for l in labels_response.labels[:10]]
    avg_confidence = sum(l.confidence for l in labels_response.labels) / max(
        len(labels_response.labels), 1
    )

    return ImageDescriptionResponse(
        description=description,
        tags=tags,
        confidence=avg_confidence,
        model="amazon-rekognition",
    )


def describe_image_from_file(
    image_path: str, confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> ImageDescriptionResponse:
    image_bytes, fmt = encode_image_to_bytes(image_path)
    request = ImageAnalysisRequest(image_bytes=image_bytes, image_format=fmt)
    return describe_image(request, confidence_threshold=confidence_threshold)


def describe_image_from_url(
    image_url: str, confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> ImageDescriptionResponse:
    image_bytes, fmt = encode_image_from_url(image_url)
    request = ImageAnalysisRequest(
        image_url=image_url, image_bytes=image_bytes, image_format=fmt
    )
    return describe_image(request, confidence_threshold=confidence_threshold)
