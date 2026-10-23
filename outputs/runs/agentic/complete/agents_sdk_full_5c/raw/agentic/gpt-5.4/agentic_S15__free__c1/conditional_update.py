from __future__ import annotations

from typing import Any, Dict, Optional
from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError
from database_client import get_container, get_partition_key_field
from database_models import UpdateResult


PROVIDER = "Azure Cosmos DB"


def conditional_update(primary_id: str, updates: Dict[str, Any], partition_key: Optional[str] = None, etag: Optional[str] = None) -> UpdateResult:
    container = get_container()
    partition_key_field = get_partition_key_field()
    resolved_partition_key = partition_key or primary_id

    try:
        current = container.read_item(item=primary_id, partition_key=resolved_partition_key)
    except CosmosResourceNotFoundError:
        return UpdateResult(id=primary_id, updated=False, message="document not found")

    current.update(updates)
    current["id"] = primary_id
    current[partition_key_field] = resolved_partition_key

    kwargs = {}
    if etag:
        kwargs["etag"] = etag
        kwargs["match_condition"] = MatchConditions.IfNotModified

    try:
        replaced = container.replace_item(item=primary_id, body=current, **kwargs)
    except CosmosHttpResponseError as exc:
        return UpdateResult(id=primary_id, updated=False, etag=current.get("_etag"), message=str(exc))

    return UpdateResult(id=primary_id, updated=True, etag=replaced.get("_etag"), document=replaced)
