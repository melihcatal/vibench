"""Apply a conditional or version-aware update to one stored document in Azure Cosmos DB."""
from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container, load_cosmos_config
from database_models import UpdateResult


def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None, partition_key: Optional[str] = None) -> Dict[str, Any]:
    config = load_cosmos_config()
    container = get_container(config)
    pk = partition_key or document_id
    current = container.read_item(item=document_id, partition_key=pk)
    current_version = int(current.get("version", 0))
    if expected_version is not None and current_version != expected_version:
        return UpdateResult(id=document_id, updated=False, document=current, status="version_mismatch").as_dict()
    current.update(updates)
    current["version"] = current_version + 1
    current["updated_at"] = current.get("updated_at")
    try:
        stored = container.replace_item(item=document_id, body=current)
    except CosmosHttpResponseError:
        stored = container.upsert_item(body=current, partition_key=pk)
    return UpdateResult(id=document_id, updated=True, document=stored).as_dict()
