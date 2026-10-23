from document_client import image_from_content, vision_client
from document_models import DocumentRequest, normalize_text


def extract_text(request: DocumentRequest) -> str:
    client = vision_client()
    image = image_from_content(request.content)
    response = client.text_detection(image=image)
    texts = response.text_annotations or []
    if texts:
        return normalize_text(texts[0].description)
    return ""
