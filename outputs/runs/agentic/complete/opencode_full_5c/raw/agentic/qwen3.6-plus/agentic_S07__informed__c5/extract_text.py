from document_client import (
    get_document_intelligence_client,
    analyze_document,
    build_content_type_from_path,
    DEFAULT_READ_MODEL_ID,
)
from document_models import OcrTextResult, normalize_ocr_text


def extract_text_from_file(file_path: str) -> OcrTextResult:
    content_type = build_content_type_from_path(file_path)
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return extract_text_from_bytes(file_bytes, content_type)


def extract_text_from_bytes(
    file_bytes: bytes, content_type: str = "application/pdf"
) -> OcrTextResult:
    client = get_document_intelligence_client()
    analyze_result = analyze_document(
        file_bytes=file_bytes,
        content_type=content_type,
        model_id=DEFAULT_READ_MODEL_ID,
        client=client,
    )
    return normalize_ocr_text(analyze_result)


def extract_text_from_url(file_url: str) -> OcrTextResult:
    from document_client import analyze_document_from_url

    analyze_result = analyze_document_from_url(
        file_url=file_url,
        model_id=DEFAULT_READ_MODEL_ID,
    )
    return normalize_ocr_text(analyze_result)
