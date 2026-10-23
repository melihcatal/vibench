from vision_client import VisionClient
from vision_models import normalize_safe_results

def score_image_safety(image_path):
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision safe-search annotation.
    Returns a normalized safety result dict.
    """
    client = VisionClient(service='vision')
    response = client.safe_search_detection(image_path=image_path)
    return normalize_safe_results(response)
