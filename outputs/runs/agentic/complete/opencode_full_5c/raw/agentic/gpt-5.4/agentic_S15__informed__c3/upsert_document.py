from __future__ import annotations

from typing import Any
from typing import Dict

from database_client import ensure_container
from database_client import resolve_partition_key
from database_models import UpsertResult
from database_models import normalize_document


def upsert_document(document: Dict[str, Any]) -> UpsertResult:
    container = ensure_container()
    normalized = normalize_document(document)
    normalized["partition_key"] = resolve_partition_key(normalized)
    response = container.upsert_item(body=normalized)
    headers = container.client_connection.last_response_headers
    request_charge = headers.get("x-ms-request-charge")
    return UpsertResult(
        document_id=response["id"],
        partition_key=response.get("partition_key"),
        etag=response.get("_etag"),
        request_charge=float(request_charge) if request_charge is not None else None,
        body=response,
    )
