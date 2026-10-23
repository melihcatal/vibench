from database_client import get_container, as_dict
from database_models import normalize_document_id


def conditional_update(database_name: str, container_name: str, document_id, patch):
    container = get_container(database_name, container_name)
    item_id = normalize_document_id(document_id)
    existing = container.read_item(item=item_id, partition_key=item_id)
    if "etag" in patch and existing.get("_etag") != patch["etag"]:
        raise ValueError("etag mismatch")
    existing.update({k: v for k, v in patch.items() if k != "etag"})
    updated = container.replace_item(item=item_id, body=existing)
    return as_dict(updated)
