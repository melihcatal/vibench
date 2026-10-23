from database_client import get_database_and_container

def fetch_document(document_id: str, partition_key: str):
    _, container = get_database_and_container()
    response = container.read_item(item=document_id, partition_key=partition_key)
    return response
