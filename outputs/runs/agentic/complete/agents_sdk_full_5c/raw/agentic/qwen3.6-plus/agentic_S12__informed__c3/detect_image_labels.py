"""Detect labels or objects in a static image using Google Cloud Vision.

Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model: Google Cloud Vision built-in label detection (builtin/stable)
"""

import os
from typing import List

from vision_client import create_vision_client, load_image_from_file
from vision_models import (
    ImageLabel,
    normalize_label_results,
    build_label_detection_request,
)


def detect_image_labels(
    image_path: str,
    max_results: int = 10,
) -> List[ImageLabel]:
    """Detect labels and objects in a static image using Google Cloud Vision.

    Args:
        image_path: Path to a local image file.
        max_results: Maximum number of labels to return.

    Returns:
        A list of ImageLabel objects with name, confidence, and description.
    """
    client = create_vision_client()
    image = load_image_from_file(image_path)

    request = build_label_detection_request(image, max_results=max_results)
    response = client.annotate_image(request=request)

    if response.error.message:
        raise RuntimeError(
            f"Google Cloud Vision label detection failed: {response.error.message}"
        )

    labels = normalize_label_results(response)
    return labels


def run_detect_image_labels(image_path: str) -> dict:
    """Run label detection and return a JSON-serializable result dict.

    Args:
        image_path: Path to a local image file.

    Returns:
        A dict with 'labels' (list of label dicts) and 'provider' metadata.
    """
    labels = detect_image_labels(image_path)
    return {
        "provider": "google-cloud-vision",
        "model": "builtin/stable",
        "image_path": image_path,
        "labels": [label.to_dict() for label in labels],
        "label_count": len(labels),
    }


if __name__ == "__main__":
    image_file = os.environ.get("VISION_IMAGE_PATH", "sample.jpg")
    result = run_detect_image_labels(image_file)
    print(result)
