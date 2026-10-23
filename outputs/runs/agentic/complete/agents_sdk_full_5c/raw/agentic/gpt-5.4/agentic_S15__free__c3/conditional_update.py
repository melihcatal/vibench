from __future__ import annotations

from typing import Optional

from azure.core import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError

from database_client import get_container_client
from database_models import ConditionalUpdateRequest, DocumentRecord, normalize_document


class ConditionalUpdateFailed(Exception):
    pass


def conditional_update(request: ConditionalUpdateRequest) -> Optional[DocumentRecord]:
    container = get_container_client()
    try:
        current = container.read_item(item=request.id, partition_key=request.partition_key)
    except CosmosResourceNotFoundError:
        return None

    for key, value in request.updates.items():
        current[key] = value

    kwargs = {}
    if request.expected_etag:
        kwargs["etag"] = request.expected_etag
        kwargs["match_condition"] = MatchConditions.IfNotModified

    try:
        updated = container.replace_item(item=request.id, body=current, **kwargs)
    except CosmosHttpResponseError as exc:
        raise ConditionalUpdateFailed(str(exc)) from exc

    return normalize_document(updated)
