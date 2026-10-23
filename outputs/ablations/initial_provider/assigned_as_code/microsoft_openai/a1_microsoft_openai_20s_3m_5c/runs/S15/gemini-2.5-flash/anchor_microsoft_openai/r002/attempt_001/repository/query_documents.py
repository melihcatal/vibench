from database_client import get_container_client
from database_models import Document
import os


def query_documents(query: str, partition_key: str = None):
    database_name = os.environ.get("AZURE_COSMOS_DATABASE")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER")
    if not database_name or not container_name:
        raise ValueError("AZURE_COSMOS_DATABASE and AZURE_COSMOS_CONTAINER environment variables must be set.")

    container = get_container_client(database_name, container_name)
    
    # If partition_key is provided, add it to the query options for better performance
    if partition_key:
        items = list(container.query_items(
            query=query,
            partition_key=partition_key,
            enable_cross_partition_query=False  # Should be False if partition_key is provided
        ))
    else:
        # If no partition_key, cross-partition query is needed, which is less performant
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

    return [Document.from_dict(item) for item in items]
