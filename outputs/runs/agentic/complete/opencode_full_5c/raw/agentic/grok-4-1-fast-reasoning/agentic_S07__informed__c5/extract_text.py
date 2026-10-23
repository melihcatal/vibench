from document_client import analyze_document
from document_models import get_ocr_text, OCRText


def extract_text(image_path: str) -> OCRText:
    result = analyze_document("prebuilt-document", image_path)
    return get_ocr_text(result)
