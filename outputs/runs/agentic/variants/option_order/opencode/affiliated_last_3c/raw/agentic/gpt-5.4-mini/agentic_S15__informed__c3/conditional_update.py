import json

from azure.cosmos import exceptions

from database_client import get_container
from database_models import ConditionalUpdateRequest, merge_document


def conditional_update(document_id: str, patch, etag=None, version=None):
    container = get_container()
    current = container.read_item(item=document_id, partition_key=document_id)
    req = ConditionalUpdateRequest(
        id=document_id, etag=etag, version=version, patch=patch
    )
    if req.etag and current.get("_etag") != req.etag:
        raise exceptions.CosmosHttpResponseError(message="etag mismatch")
    if req.version is not None and current.get("version") != req.version:
        raise exceptions.CosmosHttpResponseError(message="version mismatch")
    updated = merge_document(current, req.patch)
    if req.version is not None:
        updated["version"] = req.version + 1
    return container.replace_item(item=document_id, body=updated)


def main(payload: str) -> str:
    data = json.loads(payload)
    return json.dumps(
        conditional_update(
            data["id"], data.get("patch", {}), data.get("etag"), data.get("version")
        )
    )
