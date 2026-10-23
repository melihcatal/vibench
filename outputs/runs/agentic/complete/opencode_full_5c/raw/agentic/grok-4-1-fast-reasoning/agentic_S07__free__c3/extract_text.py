from google.cloud import vision
from document_client import load_image_bytes
from document_models import TextResult


def extract_text(image_path: str) -> TextResult:
    client = vision.ImageAnnotatorClient()
    content = load_image_bytes(image_path)
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text if response.full_text_annotation else ""
    return {"text": text.strip()}
