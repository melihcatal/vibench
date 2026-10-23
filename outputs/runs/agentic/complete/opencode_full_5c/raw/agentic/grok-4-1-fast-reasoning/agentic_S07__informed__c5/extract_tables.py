from document_client import analyze_document
from document_models import get_ocr_tables, OCRTable


def extract_tables(image_path: str) -> list[OCRTable]:
    result = analyze_document("prebuilt-document", image_path)
    return get_ocr_tables(result)
