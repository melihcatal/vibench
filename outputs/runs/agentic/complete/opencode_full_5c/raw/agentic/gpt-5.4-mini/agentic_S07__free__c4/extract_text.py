from google.cloud import vision

from document_client import normalize_text, vision_client
from document_models import DocumentRequest, TextResponse


def extract_text(request: DocumentRequest) -> TextResponse:
    client = vision_client()
    with open(request.image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    result = client.document_text_detection(image=image)
    return TextResponse(
        text=normalize_text(
            result.full_text_annotation.text
            if result.full_text_annotation
            else result.text_annotations[0].description
            if result.text_annotations
            else ""
        )
    )
