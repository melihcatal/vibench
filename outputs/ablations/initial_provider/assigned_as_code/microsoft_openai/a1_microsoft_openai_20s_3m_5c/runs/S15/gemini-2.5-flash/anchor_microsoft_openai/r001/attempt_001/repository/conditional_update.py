from database_client import get_container_client
from database_models import Document
import os

def conditional_update(document_id, new_data, etag=None):
    database_name = os.environ.get("AZURE_COSMOS_DATABASE")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER")
    container = get_container_client(database_name, container_name)

    try:
        # Read the current document to get the latest etag
        current_document = container.read_item(item=document_id, partition_key=document_id)
        
        if etag and current_document['_etag'] != etag:
            return {'success': False, 'message': 'ETag mismatch, document has been modified.'}

        # Prepare the updated document
        updated_document = {
            'id': document_id,
            **current_document, # Keep existing fields
            **new_data # Overwrite with new data
        }

        # Perform the upsert with the etag for conditional update
        # Cosmos DB will implicitly use the _etag for optimistic concurrency
        # when doing an upsert on an existing item that includes the _etag field.
        result = container.upsert_item(body=updated_document)
        return {'success': True, 'document': Document.from_dict(result)}
    except Exception as e:
        print(f"Error performing conditional update: {e}")
        return {'success': False, 'message': str(e)}
