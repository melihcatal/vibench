from vision_client import get_vision_client
from vision_models import (
    create_image_from_bytes,
    create_feature,
    create_annotate_image_request,
    parse_text_annotations,
)
from google.cloud import vision

def detect_image_text(image_bytes: bytes):
    """Detects text appearing inside an image using Google Cloud Vision API.

    Args:
        image_bytes: The bytes of the image to analyze.

    Returns:
        A list of dictionaries, where the first element contains the full detected text
        and subsequent elements contain individual words/lines with their bounding polygons.
    """
    client = get_vision_client()
    image = create_image_from_bytes(image_bytes)
    feature = create_feature(vision.Feature.Type.TEXT_DETECTION)

    request = create_annotate_image_request(image, [feature])
    response = client.annotate_image(request)

    return parse_text_annotations(response)
