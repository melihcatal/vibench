"""Detect text appearing inside an image using Google Cloud Vision.

Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model: Google Cloud Vision built-in text detection (builtin/stable)
"""

import os
from typing import List

from vision_client import create_vision_client, load_image_from_file
from vision_models import (
    ImageTextAnnotation,
    normalize_text_detection_results,
    build_text_detection_request,
)


def detect_image_text(
    image_path: str,
) -> List[ImageTextAnnotation]:
    """Detect and extract text appearing inside a static image.

    Uses Google Cloud Vision OCR (TEXT_DETECTION) to find all text
    regions, individual words, and their bounding boxes within the image.

    Args:
        image_path: Path to a local image file.

    Returns:
        A list of ImageTextAnnotation objects with extracted text, confidence,
        and optional bounding box coordinates.
    """
    client = create_vision_client()
    image = load_image_from_file(image_path)

    request = build_text_detection_request(image)
    response = client.annotate_image(request=request)

    if response.error.message:
        raise RuntimeError(
            f"Google Cloud Vision text detection failed: {response.error.message}"
        )

    annotations = normalize_text_detection_results(response)
    return annotations


def run_detect_image_text(image_path: str) -> dict:
    """Run text detection and return a JSON-serializable result dict.

    Args:
        image_path: Path to a local image file.

    Returns:
        A dict with 'text_annotations', the full extracted text, and provider metadata.
    """
    annotations = detect_image_text(image_path)

    full_text = annotations[0].text if annotations else ""

    return {
        "provider": "google-cloud-vision",
        "model": "builtin/stable",
        "image_path": image_path,
        "full_text": full_text,
        "text_annotations": [ann.to_dict() for ann in annotations],
        "annotation_count": len(annotations),
    }


if __name__ == "__main__":
    image_file = os.environ.get("VISION_IMAGE_PATH", "sample.jpg")
    result = run_detect_image_text(image_file)
    print(result)
