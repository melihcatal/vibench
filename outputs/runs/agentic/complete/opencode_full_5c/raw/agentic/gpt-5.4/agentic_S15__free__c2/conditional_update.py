from __future__ import annotations

from typing import Any, Dict, Optional

from azure.core import MatchConditions
from azure.cosmos.exceptions import (
    CosmosAccessConditionFailedError,
    CosmosResourceNotFoundError,
)

from database_client import get_container
from database_models import normalize_document


def conditional_update(
    document_id: str,
    patch_operations: list[dict[str, Any]],
    partition_key: Optional[str] = None,
    etag: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    container = get_container()
    resolved_partition_key = partition_key or document_id
    kwargs: Dict[str, Any] = {}
    if etag:
        kwargs["etag"] = etag
        kwargs["match_condition"] = MatchConditions.IfNotModified
    try:
        updated = container.patch_item(
            item=document_id,
            partition_key=resolved_partition_key,
            patch_operations=patch_operations,
            **kwargs,
        )
    except CosmosResourceNotFoundError:
        return None
    except CosmosAccessConditionFailedError as exc:
        raise RuntimeError(
            f"Azure Cosmos DB conditional update failed due to ETag mismatch: {exc.message}"
        ) from exc
    return normalize_document(updated)
