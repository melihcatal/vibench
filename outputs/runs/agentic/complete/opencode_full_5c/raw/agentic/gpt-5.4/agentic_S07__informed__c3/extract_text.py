from __future__ import annotations

from document_client import DEFAULT_MODEL_ID, analyze_document
from document_models import DocumentRequest, normalize_text


def extract_text(
    file_path: str, locale: str | None = None, pages: str | None = None
) -> str:
    request = DocumentRequest(
        file_path=file_path, model_id=DEFAULT_MODEL_ID, locale=locale, pages=pages
    )
    result = analyze_document(
        request.file_path, model_id=request.model_id, **request.as_kwargs()
    )
    return normalize_text(result)
