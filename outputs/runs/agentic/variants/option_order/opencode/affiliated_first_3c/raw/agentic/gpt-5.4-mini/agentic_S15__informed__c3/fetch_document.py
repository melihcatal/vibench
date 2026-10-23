from database_client import get_container


def fetch_document(document_id, partition_key=None):
    container = get_container()
    pk = document_id if partition_key is None else partition_key
    return container.read_item(item=document_id, partition_key=pk)
