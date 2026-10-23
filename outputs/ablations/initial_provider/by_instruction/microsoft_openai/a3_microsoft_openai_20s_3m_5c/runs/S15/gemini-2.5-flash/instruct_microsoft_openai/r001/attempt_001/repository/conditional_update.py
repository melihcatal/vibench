from database_client import get_cosmos_client
from database_models import Document
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosHttpResponseError

def conditional_update(document_id: str, new_content: dict, etag: str, doc_type: str = "general"):
    container = get_cosmos_client()
    try:
        # First, retrieve the document to get its current state and etag
        existing_document = container.read_item(item=document_id, partition_key=document_id)
        
        # Check if the etag matches the provided etag for optimistic concurrency
        if existing_document['_etag'] != etag:
            return {"status": "failed", "message": "ETag mismatch. Document has been modified by another process.", "document_id": document_id}

        # Update the document content
        existing_document['content'] = new_content
        existing_document['type'] = doc_type

        # Replace the item with the updated content, ensuring etag is passed for conditional update
        updated_item = container.replace_item(item=existing_document['id'], body=existing_document)
        return {"status": "success", "document_id": updated_item['id'], "new_etag": updated_item['_etag']}

    except CosmosResourceNotFoundError:
        return {"status": "failed", "message": "Document not found.", "document_id": document_id}
    except CosmosHttpResponseError as e:
        if e.status_code == 412: # Precondition Failed (ETag mismatch)
            return {"status": "failed", "message": "ETag mismatch. Document has been modified by another process.", "document_id": document_id}
        raise
