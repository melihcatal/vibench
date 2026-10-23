from google.cloud import vision

from document_client import vision_client, vision_image_from_request
from document_models import OCRRequest, OCRResponse, normalize_text


def extract_text(request: OCRRequest) -> OCRResponse:
    client = vision_client()
    image = vision_image_from_request(request.image_uri, request.image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations or []
    text = normalize_text(texts[0].description if texts else "")
    return OCRResponse(text=text, raw={"provider": "google_cloud_vision", "annotations": [x.description for x in texts]})
