import os
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import TextDetectionResponse

def detect_image_text(image_path: str) -> TextDetectionResponse:
    """Detects text in a static image using Google Cloud Vision API."""
    client = get_vision_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision_v1.Image(content=content)
    response = client.text_detection(image=image)
    
    return TextDetectionResponse(
        provider="google-cloud-vision",
        text="\n".join([text.description for text in response.text_annotations[1:]]),
        full_text=response.full_text_annotation.text if response.full_text_annotation else ""
    )