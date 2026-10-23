from google.cloud import vision_v1
from document_client import get_vision_client
from document_models import TextExtractionResult

def extract_plain_text_from_image(image_bytes: bytes) -> TextExtractionResult:
    client = get_vision_client()
    image = vision_v1.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        full_text = texts[0].description
        language_codes = [response.full_text_annotation.language_codes[0]] if response.full_text_annotation and response.full_text_annotation.language_codes else []
        return TextExtractionResult(text_content=full_text, language_codes=language_codes)
    else:
        return TextExtractionResult(text_content="", language_codes=[])