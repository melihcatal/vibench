from __future__ import annotations

from typing import Any, Dict, List

from azure.core import MatchConditions

from database_client import get_container_client
from database_models import DocumentConditionalUpdateRequest, parse_document_response


def conditional_update(
    document_id: str,
    patch_operations: List[Dict[str, Any]],
    partition_key: str | None = None,
    etag: str | None = None,
):
    request = DocumentConditionalUpdateRequest(
        document_id=document_id,
        patch_operations=patch_operations,
        partition_key=partition_key,
        etag=etag,
    )
    container = get_container_client()
    kwargs = {}
    if request.etag:
        kwargs["etag"] = request.etag
        kwargs["match_condition"] = MatchConditions.IfNotModified
    response = container.patch_item(
        item=request.document_id,
        partition_key=request.partition_key or request.document_id,
        patch_operations=request.patch_operations,
        **kwargs,
    )
    return parse_document_response(response)
