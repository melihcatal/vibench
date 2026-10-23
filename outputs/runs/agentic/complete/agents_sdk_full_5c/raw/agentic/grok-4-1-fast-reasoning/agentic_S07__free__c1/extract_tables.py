from document_client import analyze_document
from document_models import extract_tables
from typing import List

def extract_tables(image_path: str) -> List[List[List[str]]]:
    """
    Extracts table cells and row structure from a document.
    """
    response = analyze_document(image_path, ['TABLES'])
    return extract_tables(response)
