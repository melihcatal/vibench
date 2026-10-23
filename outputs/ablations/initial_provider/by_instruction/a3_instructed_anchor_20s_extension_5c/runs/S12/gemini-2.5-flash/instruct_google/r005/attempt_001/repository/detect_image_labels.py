from vision_client import get_vision_client
from vision_models import create_image_from_bytes, create_feature, parse_label_annotations
from google.cloud import vision

def detect_image_labels(image_content: bytes) -> list:
    client = get_vision_client()
    image = create_image_from_bytes(image_content)
    feature = create_feature(vision.Feature.Type.LABEL_DETECTION)
    response = client.annotate_image(request={'image': image, 'features': [feature]})
    return parse_label_annotations(response)
