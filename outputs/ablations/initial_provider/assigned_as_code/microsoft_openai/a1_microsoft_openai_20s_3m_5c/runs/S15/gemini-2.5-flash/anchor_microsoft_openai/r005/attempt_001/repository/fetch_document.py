from database_client import get_container_client


def fetch_document(document_id, database_name, container_name, partition_key=None):
    container = get_container_client(database_name, container_name)
    if partition_key:
        document = container.read_item(item=document_id, partition_key=partition_key)
    else:
        document = container.read_item(item=document_id, partition_key=document_id) # Assuming id is partition key if not specified
    return document
