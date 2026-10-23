import io
from google.cloud import vision
from document_client import get_vision_client
from document_models import DocumentTextExtractionResponse


def extract_text_from_image(image_content: bytes) -> DocumentTextExtractionResponse:
    client = get_vision_client()

    image = vision.Image(content=image_content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    full_text = ""
    if texts:
        full_text = texts[0].description  # First annotation is the full text

    return DocumentTextExtractionResponse(text_content=full_text)
