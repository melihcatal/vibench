from azure.cosmos import MatchConditions
from database_client import get_container_client
from database_models import normalize_document, normalize_id


def conditional_update(payload, config=None):
    container = get_container_client(config)
    document = normalize_document(payload)
    document_id = normalize_id(payload)
    etag = payload.get('etag')
    condition = MatchConditions.IfNotModified if etag else None
    options = {'etag': etag} if etag else {}
    updated = container.replace_item(item=document_id, body=document, etag=etag, match_condition=condition, **options)
    return updated
