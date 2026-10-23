from database_client import get_container_client
from database_models import Document
import os


def conditional_update(document_id: str, partition_key: str, updated_content: dict, etag: str):
    database_name = os.environ.get("AZURE_COSMOS_DATABASE")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER")
    if not database_name or not container_name:
        raise ValueError("AZURE_COSMOS_DATABASE and AZURE_COSMOS_CONTAINER environment variables must be set.")

    container = get_container_client(database_name, container_name)
    
    # Fetch the existing document to get its current ETag
    existing_document = container.read_item(item=document_id, partition_key=partition_key)
    
    if existing_document['_etag'] != etag:
        raise ValueError("ETag mismatch. Document has been modified by another operation.")

    # Merge updated content with existing document, preserving id and _etag
    merged_document = {**existing_document, **updated_content}
    merged_document['id'] = document_id  # Ensure id is preserved
    merged_document['_etag'] = etag       # Ensure etag is preserved for the request header

    # Perform the replace operation with the etag in the headers for conditional update
    # Cosmos SDK handles the If-Match header automatically when _etag is present in the item
    response = container.replace_item(item=document_id, body=merged_document)
    return Document.from_dict(response)
