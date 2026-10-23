from database_client import client, database_name, container_name


def fetch_document(document_id: str):
    container = client.get_database_client(database_name).get_container_client(
        container_name
    )
    item = container.read_item(
        item=document_id, partition_key=PartitionKey(document_id)
    )
    return item
