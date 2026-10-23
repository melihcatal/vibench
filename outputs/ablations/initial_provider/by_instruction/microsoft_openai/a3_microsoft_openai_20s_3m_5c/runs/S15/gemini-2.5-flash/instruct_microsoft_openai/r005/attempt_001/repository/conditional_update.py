from database_client import get_database_and_container
import os

def conditional_update(database_name: str, container_name: str, document_id: str, new_content: dict, etag: str, partition_key: str = None):
    container = get_database_and_container(database_name, container_name)

    # When updating, we need to pass the etag in the headers for optimistic concurrency control.
    # The new_content should also include the 'id' field.
    new_content["id"] = document_id
    
    options = {'if_match': etag}
    if partition_key:
        options['partitionKey'] = partition_key

    response = container.replace_item(item=document_id, body=new_content, options=options)
    return response

if __name__ == "__main__":
    database_name = os.environ.get("COSMOS_DB_DATABASE_NAME", "YourDatabaseName")
    container_name = os.environ.get("COSMOS_DB_CONTAINER_NAME", "YourContainerName")
    sample_document_id = "doc1"

    # For a real scenario, you would first fetch the document to get its current etag.
    # This is a placeholder for demonstration.
    # Let's assume we fetched a document and got this etag and current content.
    # In a real application, you would use fetch_document to get the etag and current_content.

    # --- Simulate fetching a document to get its etag ---
    # In a real app, you would do this:
    # from fetch_document import fetch_document
    # existing_doc = fetch_document(database_name, container_name, sample_document_id)
    # if existing_doc:
    #     current_etag = existing_doc['_etag']
    #     current_content = {k: v for k, v in existing_doc.items() if not k.startswith('_')}
    # else:
    #     print("Document not found for conditional update example.")
    #     exit()
    
    # For this example, let's just make up an etag and some content assuming it exists and we have its etag.
    # This will likely fail if the etag doesn't match a real document in your Cosmos DB.
    dummy_etag = "dummy_etag_from_previous_read"
    updated_content = {"id": sample_document_id, "name": "Updated Test Document", "value": 456, "status": "processed"}

    print("WARNING: This example will likely fail if the provided 'dummy_etag' does not match an actual document's etag in your Cosmos DB. You should fetch the document first to get a real etag.")

    try:
        # Assuming a partition key might be the document_id itself or another field.
        # If your container has a different partition key, provide it here.
        response = conditional_update(database_name, container_name, sample_document_id, updated_content, dummy_etag, partition_key=sample_document_id)
        print(f"Document conditionally updated successfully. New ETag: {response.get('_etag')}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during conditional update: {e}")
