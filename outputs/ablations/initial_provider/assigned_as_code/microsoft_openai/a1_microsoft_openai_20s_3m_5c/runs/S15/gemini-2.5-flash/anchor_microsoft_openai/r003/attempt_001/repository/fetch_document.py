from database_client import get_cosmos_client, get_container
import os

def fetch_document(document_id, partition_key, config=None):
    config = config or {}
    client = get_cosmos_client(config)
    container_name = config.get('container', os.environ.get('AZURE_COSMOS_CONTAINER'))
    database_name = config.get('database', os.environ.get('AZURE_COSMOS_DATABASE'))

    if not container_name or not database_name:
        raise ValueError("Azure Cosmos DB database and container names must be provided or set in environment variables.")

    container = get_container(client, database_name, container_name)
    
    # Assuming document_id is also the item_id for read_item
    response = container.read_item(item=document_id, partition_key=partition_key)
    return response
