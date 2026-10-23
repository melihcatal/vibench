from database_client import get_container_client
from azure.cosmos.exceptions import CosmosResourceExistsError, CosmosHttpResponseError


def conditional_update(document_id, updated_document, database_name, container_name, partition_key=None, etag=None):
    container = get_container_client(database_name, container_name)
    
    # Cosmos DB handles optimistic concurrency with ETag implicitly on replace_item
    # If the item's ETag in the database doesn't match the ETag provided in the request
    # (via _etag field in updated_document), it will raise a 412 Precondition Failed error.
    if etag:
        updated_document['_etag'] = etag

    try:
        if partition_key:
            response = container.replace_item(item=document_id, body=updated_document, partition_key=partition_key)
        else:
            response = container.replace_item(item=document_id, body=updated_document) # Assumes id is partition key if not specified
        return {"status": "success", "document": response}
    except CosmosHttpResponseError as e:
        if e.status_code == 412:  # Precondition Failed
            return {"status": "failed", "message": "Document ETag mismatch. The document has been modified by another operation.", "error": str(e)}
        else:
            raise e
