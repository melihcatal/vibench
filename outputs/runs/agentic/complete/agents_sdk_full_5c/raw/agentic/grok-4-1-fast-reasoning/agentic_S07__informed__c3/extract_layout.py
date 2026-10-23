from document_client import analyze_document
from document_models import extract_layout_elements

def extract_layout(image_path: str) -> dict:
    result = analyze_document("prebuilt-layout", image_path)
    return extract_layout_elements(result)