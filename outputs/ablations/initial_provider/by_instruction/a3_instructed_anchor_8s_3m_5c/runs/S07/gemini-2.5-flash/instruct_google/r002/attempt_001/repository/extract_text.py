from google.cloud import vision
from document_client import DocumentClient
from document_models import DocumentRequest, TextExtractionResponse

def extract_text_from_image(image_content: bytes) -> TextExtractionResponse:
    client = DocumentClient()
    image = vision.Image(content=image_content)

    response = client.client.document_text_detection(image=image)
    full_text = response.full_text_annotation.text

    return TextExtractionResponse(text=full_text, full_response=response._pb)
