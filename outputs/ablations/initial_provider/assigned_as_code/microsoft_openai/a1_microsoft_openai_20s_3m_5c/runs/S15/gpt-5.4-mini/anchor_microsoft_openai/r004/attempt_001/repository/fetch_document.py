from database_client import get_container_client
from database_models import normalize_id


def fetch_document(payload, config=None):
    container = get_container_client(config)
    document_id = normalize_id(payload)
    item = container.read_item(item=document_id, partition_key=payload.get('partition_key', document_id))
    return item
