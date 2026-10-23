from document_client import analyze_document
from document_models import extract_tables

def extract_tables(image_path: str) -> list:
    result = analyze_document("prebuilt-layout", image_path)
    return extract_tables(result)