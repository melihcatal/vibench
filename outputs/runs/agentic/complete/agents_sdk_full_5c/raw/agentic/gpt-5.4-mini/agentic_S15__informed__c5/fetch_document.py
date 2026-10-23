from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container_client
from database_models import NormalizedResponse


def fetch_document(identifier: str, partition_key: Optional[str] = None, database_name: str = "documents", container_name: str = "records") -> NormalizedResponse:
    container = get_container_client(database_name, container_name)
    try:
        if partition_key is None:
            result = container.read_item(item=identifier, partition_key=identifier)
        else:
            result = container.read_item(item=identifier, partition_key=partition_key)
        return NormalizedResponse(ok=True, data=result, etag=getattr(result, "_etag", None), request_charge=getattr(result, "_request_charge", None))
    except CosmosHttpResponseError as exc:
        return NormalizedResponse(ok=False, data={"error": str(exc), "status_code": getattr(exc, "status_code", None)})
