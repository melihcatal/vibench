from google.cloud import vision
from vision_client import get_vision_client

def detect_image_text(image_bytes: bytes, config: dict = None) -> dict:
    client = get_vision_client()
    image = vision.Image(content=image_bytes)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_text = []
    if texts:
        full_text_annotation = texts[0].description
        detected_text = [text.description for text in texts[1:]] # First element is the full text

    return {"full_text": full_text_annotation, "words": detected_text}
