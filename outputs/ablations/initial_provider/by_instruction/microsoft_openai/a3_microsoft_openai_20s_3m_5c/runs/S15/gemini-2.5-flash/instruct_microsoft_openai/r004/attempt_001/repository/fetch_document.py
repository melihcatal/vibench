from database_client import CosmosDBClient
from database_models import Document
from typing import Optional

def fetch_document(document_id: str, partition_key: Optional[str] = None) -> Optional[Document]:
    cosmos_client = CosmosDBClient()
    try:
        # partition_key is required for point reads in Cosmos DB if it's defined for the container
        if partition_key:
            response = cosmos_client.container.read_item(item=document_id, partition_key=partition_key)
        else:
            # Attempt to read without partition key, might fail if container requires it
            response = cosmos_client.container.read_item(item=document_id, partition_key=document_id) # Often id is used as partition key for simplicity
        return Document.from_dict(response)
    except Exception as e:
        print(f"Error fetching document: {e}")
        return None
