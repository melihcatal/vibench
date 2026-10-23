from document_client import get_vision_client
from document_models import DocumentTextExtractionResponse
from google.cloud import vision_v1


def extract_text_from_image(image_content: bytes) -> DocumentTextExtractionResponse:
    client = get_vision_client()
    image = vision_v1.Image(content=image_content)

    response = client.document_text_detection(image=image)
    full_text = response.full_text_annotation.text

    return DocumentTextExtractionResponse(text=full_text)
