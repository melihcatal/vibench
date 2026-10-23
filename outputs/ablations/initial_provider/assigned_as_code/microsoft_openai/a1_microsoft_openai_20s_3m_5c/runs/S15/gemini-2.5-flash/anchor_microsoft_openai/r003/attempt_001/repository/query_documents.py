from database_client import get_cosmos_client, get_container
import os

def query_documents(query_string, partition_key=None, config=None):
    config = config or {}
    client = get_cosmos_client(config)
    container_name = config.get('container', os.environ.get('AZURE_COSMOS_CONTAINER'))
    database_name = config.get('database', os.environ.get('AZURE_COSMOS_DATABASE'))

    if not container_name or not database_name:
        raise ValueError("Azure Cosmos DB database and container names must be provided or set in environment variables.")

    container = get_container(client, database_name, container_name)
    
    # Example query: SELECT * FROM c WHERE c.someField = 'someValue'
    # For partition-style key queries, the partition_key parameter to read_item is more direct.
    # For general field value queries, use query_items.
    items = list(container.query_items(
        query=query_string,
        partition_key=partition_key, # Can be None for cross-partition queries, but better to provide if known
        enable_cross_partition_query=True # Enable if cross-partition query is expected
    ))
    return items
