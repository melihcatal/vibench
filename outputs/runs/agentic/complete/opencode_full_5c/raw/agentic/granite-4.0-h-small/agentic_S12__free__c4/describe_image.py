# describe_image.py
# [SAME-SCENARIO] Generate a short visual description for an image

from vision_client import get_client, load_image_bytes, PROVIDER
from vision_models import (
    ImageAnnotateRequest,
    ImageAnnotateResponse,
    normalize_response,
)

import json


def describe_image(image_path: str) -> str:
    """
    Produce a concise one‑sentence description of the image.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        str: Human‑readable description.
    """
    img_bytes = load_image_bytes(image_path)
    client = get_client()
    request = ImageAnnotateRequest(img_bytes, features=[{"type": "DESCRIPTION"}])
    vision_response = client.annotate_image(
        {"image": {"content": request.image_bytes}, "features": request.features}
    )
    response = normalize_response(PROVIDER, vision_response.to_dict())
    return response.description or "No description available."
