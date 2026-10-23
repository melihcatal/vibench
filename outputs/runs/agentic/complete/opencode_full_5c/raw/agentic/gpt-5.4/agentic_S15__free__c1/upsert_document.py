from __future__ import annotations

from typing import Any

from database_client import ensure_container, extract_cosmos_headers
from database_models import OperationResult, normalize_document


def upsert_document(document: dict[str, Any]) -> OperationResult:
    container = ensure_container()
    normalized = normalize_document(document)
    response = container.upsert_item(body=normalized)
    headers = extract_cosmos_headers(container.client_connection.last_response_headers)
    return OperationResult(
        provider="azure_cosmos_db",
        success=True,
        document=response,
        request_charge=headers["request_charge"],
        etag=headers["etag"],
    )
