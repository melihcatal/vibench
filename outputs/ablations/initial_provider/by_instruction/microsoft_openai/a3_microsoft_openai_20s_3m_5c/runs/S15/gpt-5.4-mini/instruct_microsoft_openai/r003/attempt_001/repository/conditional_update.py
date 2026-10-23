from azure.cosmos import MatchConditions

from database_client import get_container
from database_models import build_response, normalize_document, normalize_id


def conditional_update(document_id, partition_key, updates, etag=None):
    container = get_container()
    existing = container.read_item(item=normalize_id(document_id), partition_key=partition_key)
    existing.update(normalize_document(updates))
    kwargs = {}
    if etag:
        kwargs["etag"] = etag
        kwargs["match_condition"] = MatchConditions.IfNotModified
    result = container.replace_item(item=existing, body=existing, **kwargs)
    return build_response(result)
