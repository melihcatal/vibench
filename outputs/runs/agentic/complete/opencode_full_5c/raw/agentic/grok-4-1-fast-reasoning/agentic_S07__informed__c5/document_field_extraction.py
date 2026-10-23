from document_client import analyze_document
from document_models import parse_invoice_fields


def document_field_extraction(image_path: str) -> dict:
    result = analyze_document("prebuilt-invoice", image_path)
    return parse_invoice_fields(result)
