from typing import Any, Dict, List

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_cosmos_container
from database_models import ConditionalUpdateRequest


def conditional_update(
    document_id: Any,
    patch_operations: List[Dict[str, Any]],
    partition_key: Any = None,
    etag: str | None = None,
) -> Dict[str, Any]:
    request = ConditionalUpdateRequest.create(
        document_id=document_id,
        partition_key=partition_key,
        patch_operations=patch_operations,
        etag=etag,
    )
    container = get_cosmos_container()
    kwargs = {}
    if request.etag:
        kwargs["etag"] = request.etag
        kwargs["match_condition"] = MatchConditions.IfNotModified
    try:
        response = container.patch_item(
            item=request.document_id,
            partition_key=request.partition_key,
            patch_operations=request.patch_operations,
            **kwargs,
        )
        return {
            "provider": "azure-cosmos-db",
            "updated": True,
            "document": response,
            "etag": response.get("_etag"),
        }
    except CosmosHttpResponseError as exc:
        status_code = getattr(exc, "status_code", None)
        if status_code == 412:
            return {
                "provider": "azure-cosmos-db",
                "updated": False,
                "reason": "etag_mismatch",
                "status_code": status_code,
            }
        raise
