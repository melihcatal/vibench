from database_client import get_cosmos_client, get_container
import os

def conditional_update(document_id, partition_key, new_data, etag, config=None):
    config = config or {}
    client = get_cosmos_client(config)
    container_name = config.get('container', os.environ.get('AZURE_COSMOS_CONTAINER'))
    database_name = config.get('database', os.environ.get('AZURE_COSMOS_DATABASE'))

    if not container_name or not database_name:
        raise ValueError("Azure Cosmos DB database and container names must be provided or set in environment variables.")

    container = get_container(client, database_name, container_name)

    # Fetch the existing document to get its current state and ETag
    # Optimistic concurrency control using ETag
    # The new_data will be merged with the existing document
    
    # First, try to read the item. If it doesn't exist, this might not be a true update.
    # For a conditional update, we often need the current ETag.
    try:
        # read_item requires partition_key
        existing_item = container.read_item(item=document_id, partition_key=partition_key)
    except Exception as e:
        # Handle case where item might not exist or other errors
        raise RuntimeError(f"Failed to read document {document_id} for conditional update: {e}")

    if existing_item['_etag'] != etag:
        raise ValueError("ETag mismatch. Document has been modified by another operation.")

    # Merge new_data into existing_item
    updated_item = {**existing_item, **new_data, 'id': document_id}

    # Perform the upsert with the ETag from the read operation
    # This will fail if the item's ETag has changed since it was read.
    response = container.upsert_item(body=updated_item, matching_headers={'If-Match': etag})
    
    return response
