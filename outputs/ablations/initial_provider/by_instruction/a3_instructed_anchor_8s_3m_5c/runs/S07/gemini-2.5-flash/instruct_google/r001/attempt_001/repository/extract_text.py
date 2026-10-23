from document_client import get_document_vision_client
from document_models import ExtractedText
from google.cloud import vision

def extract_plain_text(image_content: bytes) -> ExtractedText:
    client = get_document_vision_client()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
        return ExtractedText(full_text)
    else:
        return ExtractedText("")
