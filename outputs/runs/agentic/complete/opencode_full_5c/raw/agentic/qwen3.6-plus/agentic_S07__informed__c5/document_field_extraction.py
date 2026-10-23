from document_client import (
    get_document_intelligence_client,
    analyze_document,
    build_content_type_from_path,
)
from document_models import FieldExtractionResult, normalize_field_extraction_result

INVOICE_MODEL_ID = "prebuilt-invoice"


def extract_document_fields_from_file(file_path: str) -> FieldExtractionResult:
    content_type = build_content_type_from_path(file_path)
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return extract_document_fields_from_bytes(file_bytes, content_type)


def extract_document_fields_from_bytes(
    file_bytes: bytes,
    content_type: str = "application/pdf",
    model_id: str = INVOICE_MODEL_ID,
) -> FieldExtractionResult:
    client = get_document_intelligence_client()
    analyze_result = analyze_document(
        file_bytes=file_bytes,
        content_type=content_type,
        model_id=model_id,
        client=client,
    )
    return normalize_field_extraction_result(analyze_result)


def extract_document_fields_from_url(
    file_url: str,
    model_id: str = INVOICE_MODEL_ID,
) -> FieldExtractionResult:
    from document_client import analyze_document_from_url

    analyze_result = analyze_document_from_url(
        file_url=file_url,
        model_id=model_id,
    )
    return normalize_field_extraction_result(analyze_result)
