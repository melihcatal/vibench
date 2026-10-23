import os
from .document_client import LayoutClient
from .document_models import LayoutResult

def extract_layout(image_path: str) -> LayoutResult:
    """Extract layout blocks, lines, and tables from a document using Google Vision Document AI.
    """
    client = LayoutClient()
    response = client.process_document(image_path)
    return LayoutResult(blocks=response.get('pages', [{}])[0].get('layout', []))