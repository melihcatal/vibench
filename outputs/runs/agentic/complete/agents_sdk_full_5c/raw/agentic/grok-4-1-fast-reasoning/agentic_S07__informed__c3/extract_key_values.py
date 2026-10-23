from document_client import analyze_document
from document_models import extract_key_values

def extract_key_values(image_path: str) -> dict:
    result = analyze_document("prebuilt-receipt", image_path)
    return extract_key_values(result)