from database_client import get_container
from database_models import normalize_document, normalize_document_id


def upsert_document(database_name: str, container_name: str, document_id, document):
    container = get_container(database_name, container_name)
    payload = normalize_document(document)
    payload["id"] = normalize_document_id(document_id)
    return container.upsert_item(payload)
