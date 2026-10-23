from __future__ import annotations

from document_client import KEY_VALUE_MODEL_ID, analyze_document
from document_models import DocumentRequest, normalize_key_value_pairs


def extract_key_values(
    file_path: str, locale: str | None = None, pages: str | None = None
) -> list[dict]:
    request = DocumentRequest(
        file_path=file_path, model_id=KEY_VALUE_MODEL_ID, locale=locale, pages=pages
    )
    result = analyze_document(
        request.file_path, model_id=request.model_id, **request.as_kwargs()
    )
    return normalize_key_value_pairs(result)
