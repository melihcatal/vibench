from document_client import (
    get_document_intelligence_client,
    analyze_document,
    build_content_type_from_path,
    DEFAULT_MODEL_ID,
)
from document_models import TableResult, normalize_table_result


def extract_tables_from_file(file_path: str) -> list[TableResult]:
    content_type = build_content_type_from_path(file_path)
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return extract_tables_from_bytes(file_bytes, content_type)


def extract_tables_from_bytes(
    file_bytes: bytes, content_type: str = "application/pdf"
) -> list[TableResult]:
    client = get_document_intelligence_client()
    analyze_result = analyze_document(
        file_bytes=file_bytes,
        content_type=content_type,
        model_id=DEFAULT_MODEL_ID,
        client=client,
    )
    tables = []
    if hasattr(analyze_result, "tables") and analyze_result.tables:
        for table_obj in analyze_result.tables:
            tables.append(normalize_table_result(table_obj))
    return tables


def extract_tables_from_url(file_url: str) -> list[TableResult]:
    from document_client import analyze_document_from_url

    analyze_result = analyze_document_from_url(
        file_url=file_url,
        model_id=DEFAULT_MODEL_ID,
    )
    tables = []
    if hasattr(analyze_result, "tables") and analyze_result.tables:
        for table_obj in analyze_result.tables:
            tables.append(normalize_table_result(table_obj))
    return tables
