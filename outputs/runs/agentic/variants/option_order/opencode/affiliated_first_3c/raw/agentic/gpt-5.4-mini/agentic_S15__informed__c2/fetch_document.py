from database_client import get_container, as_dict
from database_models import normalize_document_id


def fetch_document(database_name: str, container_name: str, document_id):
    container = get_container(database_name, container_name)
    item = container.read_item(
        item=normalize_document_id(document_id),
        partition_key=normalize_document_id(document_id),
    )
    return as_dict(item)
