from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Optional

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container_client
from database_models import FetchResult


def fetch_document(document_id: str, partition_key: str) -> FetchResult:
    container = get_container_client()
    try:
        response: Dict[str, Any] = container.read_item(
            item=str(document_id), partition_key=str(partition_key)
        )
        return FetchResult(
            found=True,
            document_id=response["id"],
            partition_key=response.get("partition_key"),
            etag=response.get("_etag"),
            body=response,
        )
    except CosmosResourceNotFoundError:
        return FetchResult(
            found=False,
            document_id=str(document_id),
            partition_key=str(partition_key),
            etag=None,
            body=None,
        )
