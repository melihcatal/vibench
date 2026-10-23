# detect_image_text.py
# [SAME-SCENARIO] Detect text appearing inside an image

from vision_client import get_client, load_image_bytes, PROVIDER
from vision_models import (
    ImageAnnotateRequest,
    ImageAnnotateResponse,
    normalize_response,
)


def detect_text(image_path: str) -> str:
    """
    Extract OCR text from the supplied image.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        str: Extracted text (or empty string if none).
    """
    img_bytes = load_image_bytes(image_path)
    client = get_client()
    request = ImageAnnotateRequest(img_bytes, features=[{"type": "TEXT_DETECTION"}])
    vision_response = client.annotate_image(
        {"image": {"content": request.image_bytes}, "features": request.features}
    )
    response = normalize_response(PROVIDER, vision_response.to_dict())
    return response.text or ""
