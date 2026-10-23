from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosAccessConditionFailedError, CosmosResourceNotFoundError

from database_client import get_container
from database_models import OperationResult, normalize_document


def conditional_update(
    document_id: str,
    partition_key: str,
    updates: Dict[str, Any],
    etag: Optional[str],
) -> OperationResult:
    container = get_container()
    try:
        current = container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return OperationResult(success=False, status_message="Document not found in Azure Cosmos DB")

    current.update(updates)
    try:
        replaced = container.replace_item(
            item=document_id,
            body=current,
            etag=etag,
            match_condition=MatchConditions.IfNotModified,
        )
    except CosmosAccessConditionFailedError:
        return OperationResult(success=False, status_message="ETag mismatch during Azure Cosmos DB conditional update")

    return OperationResult(
        success=True,
        document=normalize_document(replaced),
        etag=replaced.get("_etag"),
        status_message="Conditionally updated document in Azure Cosmos DB",
    )
