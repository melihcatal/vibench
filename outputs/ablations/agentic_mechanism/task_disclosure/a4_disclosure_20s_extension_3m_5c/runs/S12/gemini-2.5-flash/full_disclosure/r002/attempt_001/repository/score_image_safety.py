from google.cloud import vision_v1
from google.oauth2 import service_account
import os

def score_image_safety(image_content: bytes):
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI Safe Search Detection.

    Args:
        image_content: The content of the image as bytes.

    Returns:
        A dictionary containing the safe search annotation results.
    """
    # Authenticate using service account credentials from an environment variable
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service_account_key.json"
    
    client = vision_v1.ImageAnnotatorClient()

    image = vision_v1.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe_search_annotations = response.safe_search_annotation

    result = {
        "adult": safe_search_annotations.adult.name,
        "spoof": safe_search_annotations.spoof.name,
        "medical": safe_search_annotations.medical.name,
        "violence": safe_search_annotations.violence.name,
        "racy": safe_search_annotations.racy.name,
    }
    return result
