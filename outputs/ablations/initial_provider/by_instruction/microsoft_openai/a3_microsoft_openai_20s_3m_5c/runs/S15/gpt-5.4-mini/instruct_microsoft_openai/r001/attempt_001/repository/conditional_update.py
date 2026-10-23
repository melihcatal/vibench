from azure.cosmos import MatchConditions

from database_client import get_container
from database_models import ConditionalUpdateRequest


def conditional_update(request: ConditionalUpdateRequest):
    container = get_container()
    current = container.read_item(item=request.document_id, partition_key=request.partition_key or request.document_id)
    updated = dict(current)
    updated.update(request.updates)
    if request.expected_etag:
        return container.replace_item(
            item=request.document_id,
            body=updated,
            etag=request.expected_etag,
            match_condition=MatchConditions.IfNotModified,
        )
    return container.replace_item(item=request.document_id, body=updated)
