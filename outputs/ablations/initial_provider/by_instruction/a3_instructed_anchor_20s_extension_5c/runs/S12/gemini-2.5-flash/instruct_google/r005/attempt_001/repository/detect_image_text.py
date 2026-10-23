from vision_client import get_vision_client
from vision_models import create_image_from_bytes, create_feature
from google.cloud import vision

def detect_image_text(image_content: bytes) -> str:
    client = get_vision_client()
    image = create_image_from_bytes(image_content)
    feature = create_feature(vision.Feature.Type.TEXT_DETECTION)
    response = client.annotate_image(request={'image': image, 'features': [feature]})
    if response.text_annotations:
        # The first annotation is the full text detected in the image.
        return response.text_annotations[0].description
    return "No text detected."
