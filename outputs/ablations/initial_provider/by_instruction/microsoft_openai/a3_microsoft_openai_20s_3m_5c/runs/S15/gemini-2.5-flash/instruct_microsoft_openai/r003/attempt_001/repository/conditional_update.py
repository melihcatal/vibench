from database_client import CosmosDBClient
from database_models import Document
from azure.cosmos.exceptions import CosmosHttpResponseError

def conditional_update(document: Document):
    client = CosmosDBClient()
    container = client.get_container()
    
    # When _etag is provided, Cosmos DB will perform optimistic concurrency control
    # The update will only succeed if the _etag matches the one on the server
    headers = {"If-Match": document._etag} if document._etag else None
    
    try:
        # Cosmos DB replace_item implicitly handles conditional update with _etag in headers
        # The document passed to replace_item must contain the partition key and id.
        # The document.to_dict() should include the _etag for the operation to be conditional
        updated_document_dict = document.to_dict()
        if "_etag" in updated_document_dict: # _etag must not be sent in the body, it is handled via If-Match header
            del updated_document_dict["_etag"]
        
        response = container.replace_item(
            item=document.id, 
            body=updated_document_dict, 
            partition_key=document.id, # Assuming document.id is the partition key for this example
            headers=headers
        )
        return Document.from_dict(response)
    except CosmosHttpResponseError as e:
        if e.status_code == 412: # Precondition Failed (Etag mismatch)
            raise ValueError("Document ETag mismatch. The document may have been modified by another process.") from e
        raise # Re-raise other Cosmos DB errors
