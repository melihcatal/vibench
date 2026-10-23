from vision_client import VisionClient
from vision_models import normalize_text_annot

def detect_image_text(image_path):
    """Detects text appearing inside an image using Google Cloud Vision.
    Returns a list of normalized text annotation dicts.
    """
    client = VisionClient(service='vision')
    response = client.text_detection(image_path=image_path)
    return normalize_text_annot(response)
