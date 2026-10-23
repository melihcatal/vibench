from document_client import analyze_document
from document_models import get_ocr_layout, OCRLayout


def extract_layout(image_path: str) -> OCRLayout:
    result = analyze_document("prebuilt-document", image_path)
    return get_ocr_layout(result)
