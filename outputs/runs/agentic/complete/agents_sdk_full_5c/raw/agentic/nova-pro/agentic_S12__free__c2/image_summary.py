from vision_client import get_vision_client
from vision_models import VisionModels

def image_summary(image_path):
    client = get_vision_client()
    objects = client.detect_image_labels(image_path)
    description = client.describe_image(image_path)
    text = client.detect_image_text(image_path)
    safety = client.score_image_safety(image_path)
    return {'objects': objects, 'description': description, 'text': text, 'safety': safety}