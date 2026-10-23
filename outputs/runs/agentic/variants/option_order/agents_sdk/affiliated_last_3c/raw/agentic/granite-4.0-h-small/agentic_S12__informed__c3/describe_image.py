from vision_client import VisionClient
from vision_models import normalize_description

def describe_image(image_path, max_results=1):
    """Generates a short visual description for an image using Google Cloud Vision's document text feature.
    Returns a list of normalized description strings.
    """
    client = VisionClient(service='vision')
    response = client.document_text_detection(image_path=image_path)
    return normalize_description(response, max_results=max_results)
