from vision_client import get_vision_client
from vision_models import (
    create_image_from_bytes,
    create_feature,
    create_annotate_image_request,
    parse_safe_search_annotations,
)
from google.cloud import vision

def score_image_safety(image_bytes: bytes):
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API.

    Args:
        image_bytes: The bytes of the image to analyze.

    Returns:
        A dictionary with likelihood scores for different unsafe content categories (e.g., 'adult', 'violence').
    """
    client = get_vision_client()
    image = create_image_from_bytes(image_bytes)
    feature = create_feature(vision.Feature.Type.SAFE_SEARCH_DETECTION)

    request = create_annotate_image_request(image, [feature])
    response = client.annotate_image(request)

    return parse_safe_search_annotations(response)
