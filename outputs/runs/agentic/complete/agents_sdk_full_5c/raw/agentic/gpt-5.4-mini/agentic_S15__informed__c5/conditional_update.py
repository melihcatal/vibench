from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container_client
from database_models import NormalizedResponse


def conditional_update(identifier: str, patch: Dict[str, Any], partition_key: Optional[str] = None, etag: Optional[str] = None, expected_version: Optional[int] = None, database_name: str = "documents", container_name: str = "records") -> NormalizedResponse:
    container = get_container_client(database_name, container_name)
    try:
        if partition_key is None:
            current = container.read_item(item=identifier, partition_key=identifier)
            partition_key = identifier
        else:
            current = container.read_item(item=identifier, partition_key=partition_key)
        if expected_version is not None and int(current.get("version", 0)) != int(expected_version):
            return NormalizedResponse(ok=False, data={"error": "version mismatch", "current_version": current.get("version")})
        updated = dict(current)
        updated.update(patch)
        updated["id"] = identifier
        if "version" in current or expected_version is not None:
            updated["version"] = int(current.get("version", 0)) + 1
        kwargs = {"partition_key": partition_key}
        if etag:
            kwargs["match_condition"] = MatchConditions.IfNotModified
            kwargs["etag"] = etag
        result = container.replace_item(item=identifier, body=updated, **kwargs)
        return NormalizedResponse(ok=True, data=result, etag=getattr(result, "_etag", None), request_charge=getattr(result, "_request_charge", None))
    except CosmosHttpResponseError as exc:
        return NormalizedResponse(ok=False, data={"error": str(exc), "status_code": getattr(exc, "status_code", None)})
