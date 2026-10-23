from document_client import analyze_document
from document_models import get_ocr_key_values, OCRKeyValues


def extract_key_values(image_path: str) -> OCRKeyValues:
    result = analyze_document("prebuilt-document", image_path)
    return get_ocr_key_values(result)
