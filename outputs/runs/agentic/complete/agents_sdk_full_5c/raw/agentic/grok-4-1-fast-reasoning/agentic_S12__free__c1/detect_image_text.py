from google.cloud import vision
from vision_client import load_image_bytes
from vision_models import ImageText

def detect_image_text(image_path: str) -> ImageText:
    client = vision.ImageAnnotatorClient()
    image_bytes = load_image_bytes(image_path)
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    full_text = texts[0].description if texts else ""
    return ImageText(full_text=full_text)