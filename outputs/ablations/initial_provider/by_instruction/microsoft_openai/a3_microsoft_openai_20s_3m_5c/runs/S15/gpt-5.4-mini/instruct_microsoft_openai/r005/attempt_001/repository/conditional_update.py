from database_client import get_container
from database_models import build_response, normalize_document


def conditional_update(identifier, updates, etag=None):
    container = get_container()
    item_id = identifier if isinstance(identifier, str) else identifier["id"]
    current = container.read_item(item=item_id, partition_key=item_id)
    current.update(normalize_document(updates))
    kwargs = {}
    if etag:
        kwargs["etag"] = etag
        kwargs["match_condition"] = "IfNotModified"
    return container.replace_item(item=item_id, body=current, **kwargs)


def main(identifier, updates, etag=None):
    try:
        result = conditional_update(identifier, updates, etag=etag)
        return build_response(True, result)
    except Exception as exc:
        return build_response(False, error=exc)
