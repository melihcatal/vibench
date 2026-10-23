from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Optional

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container_client
from database_models import ConditionalUpdateResult


def conditional_update(
    document_id: str,
    partition_key: str,
    updates: Dict[str, Any],
    etag: Optional[str] = None,
    expected_version: Optional[int] = None,
) -> ConditionalUpdateResult:
    container = get_container_client()
    current = container.read_item(
        item=str(document_id), partition_key=str(partition_key)
    )
    if expected_version is not None and current.get("version") != expected_version:
        return ConditionalUpdateResult(
            updated=False,
            document_id=str(document_id),
            partition_key=str(partition_key),
            etag=current.get("_etag"),
            body=current,
        )
    next_document = dict(current)
    next_document.update(updates)
    next_document["id"] = str(document_id)
    next_document["partition_key"] = str(partition_key)
    next_document["version"] = int(current.get("version", 0)) + 1
    try:
        response = container.replace_item(
            item=str(document_id),
            body=next_document,
            etag=etag or current.get("_etag"),
            match_condition=MatchConditions.IfNotModified,
        )
        return ConditionalUpdateResult(
            updated=True,
            document_id=response["id"],
            partition_key=response.get("partition_key"),
            etag=response.get("_etag"),
            body=response,
        )
    except CosmosHttpResponseError:
        latest = container.read_item(
            item=str(document_id), partition_key=str(partition_key)
        )
        return ConditionalUpdateResult(
            updated=False,
            document_id=str(document_id),
            partition_key=str(partition_key),
            etag=latest.get("_etag"),
            body=latest,
        )
