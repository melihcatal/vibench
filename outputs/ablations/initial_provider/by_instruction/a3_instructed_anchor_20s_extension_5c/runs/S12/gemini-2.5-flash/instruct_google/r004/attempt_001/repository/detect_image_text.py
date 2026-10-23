from vision_client import get_vision_client
from google.cloud import vision

def detect_image_text(image_content: bytes) -> str:
    client = get_vision_client()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text annotation is the full text detected in the image
        return texts[0].description
    else:
        return "No text detected in the image."
