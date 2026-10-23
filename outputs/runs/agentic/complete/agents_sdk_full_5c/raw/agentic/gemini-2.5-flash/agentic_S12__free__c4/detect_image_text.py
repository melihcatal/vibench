from google.cloud import vision
from vision_client import get_vision_client

def detect_image_text(image_content: bytes) -> str:
    """Detects text appearing inside an image using Google Cloud Vision AI."""
    client = get_vision_client()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations if text.description]
    # The first text annotation is usually the full detected text
    if texts:
        return texts[0]
    return ""
