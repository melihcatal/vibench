from database_client import get_database_and_container
from database_models import Document

def conditional_update(document_id: str, partition_key: str, updated_data: dict, etag: str):
    _, container = get_database_and_container()
    
    # Fetch the existing document to get its ETag
    existing_document = container.read_item(item=document_id, partition_key=partition_key)

    # Update the document with new data
    existing_document.update(updated_data)

    # Perform the conditional update using the ETag
    response = container.replace_item(
        item=document_id,
        body=existing_document,
        options = {"if_match": etag}
    )
    return response
