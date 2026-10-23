from database_client import get_container
from database_models import build_response, normalize_id


def fetch_document(document_id, partition_key):
    container = get_container()
    result = container.read_item(item=normalize_id(document_id), partition_key=partition_key)
    return build_response(result)
