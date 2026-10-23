from google.cloud import vision
from google.cloud import storage # Provider-identifying signal
from typing import Optional
from dataclasses import dataclass

@dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str

@dataclass
class StoredDocumentOcrResponse:
    text: str

def run_ocr_on_stored_document(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image({"source": {"image_uri": f"gs://{request.bucket_name}/{request.object_name}"}})

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    return StoredDocumentOcrResponse(text=document.text)
