from database_client import CosmosDBClient
from database_models import Document
from typing import Any, Dict, Optional

def conditional_update(document_id: str, partition_key: str, updated_content: Dict[str, Any], etag: Optional[str] = None) -> Optional[Document]:
    cosmos_client = CosmosDBClient()
    try:
        # First, fetch the existing document to get its current state and ETag
        existing_item = cosmos_client.container.read_item(item=document_id, partition_key=partition_key)
        current_etag = existing_item["_etag"]

        if etag and current_etag != etag:
            print("ETag mismatch. Document has been modified by another process.")
            return None

        # Merge the updated content with the existing content
        existing_item.update(updated_content)
        existing_item["id"] = document_id # Ensure id is present, though read_item should return it

        # Replace the item with conditional update using the ETag
        # If the ETag provided doesn't match the one in the database, the operation will fail.
        response = cosmos_client.container.replace_item(
            item=document_id,
            body=existing_item,
            options={"IfMatch": etag or current_etag}
        )
        return Document.from_dict(response)
    except Exception as e:
        print(f"Error performing conditional update: {e}")
        return None
