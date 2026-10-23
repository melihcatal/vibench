import requests
from vision_client import VisionClient

def score_image_safety(image_path):
    """Check an image for unsafe or policy-sensitive visual content using Google Cloud Vision Safe Search.
    Returns a dict with probability scores for adult, spoof, medical, violence, and racy categories.
    """
    client = VisionClient()
    image = client.load_image(image_path)
    response = client.annotate_image({"features": [{"type": "SAFE_SEARCH_DETECTION", "maxResults": 1}]})
    safe = response.get("safeSearchAnnotation", {})
    return {
        "isAdult": safe.get("adult") == "LIKELY",
        "isViolent": safe.get("violence") == "LIKELY",
        "isRacy": safe.get("racy") == "LIKELY",
        "isMedical": safe.get("medical") == "LIKELY",
    }
