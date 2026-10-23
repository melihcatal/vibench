from azure.cosmos import CosmosClient

from database_client import get_database_endpoint, get_database_key, get_database_name, get_container_name


def fetch_document(document_id: str):
    client = CosmosClient(get_database_endpoint(), credential=get_database_key())
    container = client.get_database_client(get_database_name()).get_container_client(get_container_name())
    return container.read_item(item=document_id, partition_key=document_id)
