from __future__ import annotations

from document_client import DEFAULT_MODEL_ID, analyze_document
from document_models import DocumentRequest, normalize_tables


def extract_tables(file_path: str, pages: str | None = None) -> list[dict]:
    request = DocumentRequest(
        file_path=file_path, model_id=DEFAULT_MODEL_ID, pages=pages
    )
    result = analyze_document(
        request.file_path, model_id=request.model_id, **request.as_kwargs()
    )
    return normalize_tables(result)
