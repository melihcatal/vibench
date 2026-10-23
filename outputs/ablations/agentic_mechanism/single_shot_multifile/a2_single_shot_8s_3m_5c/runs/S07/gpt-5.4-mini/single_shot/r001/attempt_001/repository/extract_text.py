from google.cloud import vision
from document_client import get_vision_client
from document_models import DocumentOCRRequest, OCRTextResponse, normalize_text


def extract_text(request: DocumentOCRRequest) -> OCRTextResponse:
    client = get_vision_client()
    image = vision.Image(content=request.image_bytes)
    response = client.text_detection(image=image)
    annotation = response.text_annotations[0].description if response.text_annotations else ""
    return OCRTextResponse(text=normalize_text(annotation), raw=response)
