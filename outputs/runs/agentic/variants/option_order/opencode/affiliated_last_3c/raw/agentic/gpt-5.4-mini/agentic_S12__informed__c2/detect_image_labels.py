from google.cloud import vision

from vision_client import get_vision_client, make_image
from vision_models import normalize_entity


def detect_image_labels(image_path=None, image_uri=None, max_results=10):
    client = get_vision_client()
    image = make_image(image_path=image_path, image_uri=image_uri)
    response = client.label_detection(image=image, max_results=max_results)
    return [normalize_entity(entity) for entity in response.label_annotations]
