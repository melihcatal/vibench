from vision_client import VisionClient
from vision_models import normalize_labels

def detect_image_labels(image_path):
    """Detects objects/labels in a static image using Google Cloud Vision.
    Returns a list of normalized label dictionaries.
    """
    client = VisionClient(service='vision')
    response = client.label_detection(image_path=image_path)
    return normalize_labels(response)
