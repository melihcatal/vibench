from database_client import get_container
from database_models import extract_etag, normalize_document


def conditional_update(document_id, patch, partition_key=None, etag=None):
    container = get_container()
    current = container.read_item(
        item=document_id,
        partition_key=document_id if partition_key is None else partition_key,
    )
    expected = etag or extract_etag(current)
    updated = normalize_document(current)
    updated.update(normalize_document(patch))
    if expected is None:
        return container.replace_item(item=document_id, body=updated)
    return container.replace_item(
        item=document_id, body=updated, etag=expected, match_condition="IfNotModified"
    )
