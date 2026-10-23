from document_client import analyze_document
from document_models import extract_plain_text

def extract_text(image_path: str) -> str:
    result = analyze_document("prebuilt-read", image_path)
    return extract_plain_text(result)