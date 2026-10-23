from google.cloud import vision
from google.cloud import storage
import dataclasses
from typing import Optional

@dataclasses.dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str

@dataclasses.dataclass
class StoredDocumentOcrResponse:
    text_content: str

def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest
) -> StoredDocumentOcrResponse:
    """Runs OCR on a stored document object in Google Cloud Storage using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    image = vision.Image({
        'source': {'image_uri': f"gs://{request.bucket_name}/{request.object_name}"}
    })

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
    else:
        full_text = ""

    return StoredDocumentOcrResponse(
        text_content=full_text
    )
