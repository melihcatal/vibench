import os
from google.cloud import vision_v1
from document_client import get_google_vision_client
from document_models import DocumentInput, TextExtractionResult

def extract_text_from_document(doc_input: DocumentInput) -> TextExtractionResult:
    client = get_google_vision_client()

    image = vision_v1.Image(content=doc_input.document_bytes)
    
    response = client.document_text_detection(image=image)
    
    return TextExtractionResult(text=response.full_text_annotation.text)