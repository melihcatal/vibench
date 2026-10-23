from azure.cosmos import CosmosClient

from database_client import get_client


def fetch_document(document_id, config=None):
    client = get_client(config)
    container = client.get_database_client(config['database']).get_container_client(config['container'])
    return container.read_item(item=document_id, partition_key=document_id)