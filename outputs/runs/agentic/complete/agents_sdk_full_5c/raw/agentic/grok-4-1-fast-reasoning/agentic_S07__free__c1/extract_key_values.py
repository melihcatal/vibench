from document_client import analyze_document
from document_models import extract_key_value_pairs
from typing import Dict

def extract_key_values(image_path: str) -> Dict[str, str]:
    """
    Extracts key-value pairs from a form-like document.
    """
    response = analyze_document(image_path, ['FORMS'])
    return extract_key_value_pairs(response)
