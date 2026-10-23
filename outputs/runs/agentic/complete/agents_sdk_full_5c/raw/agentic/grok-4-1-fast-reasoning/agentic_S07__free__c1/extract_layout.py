from document_client import analyze_document
from document_models import extract_layout_elements
from typing import List, Dict, Any

def extract_layout(image_path: str) -> List[Dict[str, Any]]:
    """
    Extracts blocks, lines, tables, or layout elements from a document.
    """
    response = analyze_document(image_path, ['LAYOUT'])
    return extract_layout_elements(response)
