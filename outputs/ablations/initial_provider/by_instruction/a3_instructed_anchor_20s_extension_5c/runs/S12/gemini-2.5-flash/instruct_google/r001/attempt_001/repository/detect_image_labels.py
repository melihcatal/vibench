from vision_client import get_vision_client
from vision_models import (
    create_image_from_bytes,
    create_feature,
    create_annotate_image_request,
    parse_label_annotations,
)
from google.cloud import vision

def detect_image_labels(image_bytes: bytes):
    """Detects labels in a static image using Google Cloud Vision API.

    Args:
        image_bytes: The bytes of the image to analyze.

    Returns:
        A list of dictionaries, each containing 'description', 'score', and 'topicality' of the detected labels.
    """
    client = get_vision_client()
    image = create_image_from_bytes(image_bytes)
    feature = create_feature(vision.Feature.Type.LABEL_DETECTION)

    request = create_annotate_image_request(image, [feature])
    response = client.annotate_image(request)

    return parse_label_annotations(response)
