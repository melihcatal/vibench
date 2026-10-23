from typing import Dict, Optional
from database_client import DatabaseClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError


def fetch_document(
    document_id: str, partition_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Fetch a document from Azure Cosmos DB by its identifier."""
    client = DatabaseClient().get_container()
    try:
        response = client.read_item(
            item=document_id, partition_key=partition_key or document_id
        )
        return {
            "id": response["id"],
            "partition_key": response.get("partition_key"),
            "body": response,
            "etag": response.get("_etag"),
        }
    except CosmosResourceNotFoundError:
        return None
