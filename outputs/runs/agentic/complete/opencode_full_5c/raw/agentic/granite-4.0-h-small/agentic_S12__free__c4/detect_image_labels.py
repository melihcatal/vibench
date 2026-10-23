# detect_image_labels.py
# [SAME-SCENARIO] Detect labels or objects in a static image

from vision_client import get_client, load_image_bytes, PROVIDER
from vision_models import (
    ImageAnnotateRequest,
    ImageAnnotateResponse,
    normalize_response,
)

import json


def detect_labels(image_path: str) -> List[str]:
    """
    Detect visible objects/labels in the supplied image.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        List[str]: List of detected label descriptions.
    """
    # Load image bytes
    img_bytes = load_image_bytes(image_path)

    # Build client
    client = get_client()

    # Build request payload for Google Vision
    request = ImageAnnotateRequest(img_bytes, features=[{"type": "LABEL_DETECTION"}])

    # Call the Vision API
    vision_response = client.annotate_image(
        {"image": {"content": request.image_bytes}, "features": request.features}
    )

    # Normalize response to our internal model
    response = normalize_response(PROVIDER, vision_response.to_dict())

    return response.labels
