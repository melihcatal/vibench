from __future__ import annotations

from typing import Any, Dict

from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError
from azure.cosmos.match_conditions import MatchConditions

from database_client import get_container
from database_models import OperationResult, UpdateRequest, normalize_document


def conditional_update(document_id: str, partition_key: str, updates: Dict[str, Any], etag: str | None = None) -> OperationResult:
    container = get_container()
    request = UpdateRequest(id=document_id, partition_key=partition_key, updates=updates, etag=etag)
    try:
        current = container.read_item(item=request.id, partition_key=request.partition_key)
        current.update(request.updates)
        response = container.replace_item(
            item=request.id,
            body=current,
            etag=request.etag or current.get("_etag"),
            match_condition=MatchConditions.IfNotModified,
        )
        return OperationResult(
            ok=True,
            item=normalize_document(response),
            etag=response.get("_etag"),
            status_code=200,
            message="Conditionally updated in Azure Cosmos DB",
        )
    except CosmosResourceNotFoundError:
        return OperationResult(ok=False, status_code=404, message="Document not found")
    except CosmosHttpResponseError as exc:
        return OperationResult(ok=False, status_code=getattr(exc, "status_code", 412), message=str(exc))
