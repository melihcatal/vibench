import os
import json
from typing import List

from google.cloud import documentai_v1 as documentai

from document_client import DocumentClient
from document_models import OCRResult

def create_gdai_client() -> documentai.DocumentAnalyserClient:
    """Create a Google Document AI client using env credentials."""
    return documentai.DocumentAnalyserClient()

def extract_text_gdai(image_bytes: bytes) -> OCRResult:
    """Extract plain text from an image using Google Document AI."""
    client = create_gdai_client()
    parent = "projects/my-project/locations/us-central1"
    processor_path = f"{parent}/processors/document_ocr"
    response = client.analyze_document(request={'processor': processor_path, 'document': {'content': image_bytes}})
    lines = [entity.text for entity in response.document.entities if entity.type_ == documentai.SchemaType.LINE]
    return OCRResult(text=lines)
