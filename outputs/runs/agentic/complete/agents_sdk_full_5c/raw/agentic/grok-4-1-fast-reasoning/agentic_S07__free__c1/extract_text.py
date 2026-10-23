from document_client import detect_document_text
from document_models import extract_plain_text

def extract_text(image_path: str) -> str:
    """
    Extracts plain text from a scanned document image.
    """
    response = detect_document_text(image_path)
    return extract_plain_text(response)
