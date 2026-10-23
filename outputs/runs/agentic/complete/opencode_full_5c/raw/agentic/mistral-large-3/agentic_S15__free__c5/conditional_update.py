from typing import Dict, Optional, Any
from database_client import DatabaseClient
from azure.cosmos.exceptions import CosmosAccessConditionFailedError


def conditional_update(
    document_id: str,
    update_body: Dict[str, Any],
    etag: Optional[str] = None,
    partition_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Apply a conditional or version-aware update to a document in Azure Cosmos DB."""
    client = DatabaseClient().get_container()
    current_doc = client.read_item(
        item=document_id, partition_key=partition_key or document_id
    )

    updated_doc = {**current_doc, **update_body}
    if etag:
        updated_doc["_etag"] = etag

    try:
        response = client.replace_item(item=document_id, body=updated_doc, etag=etag)
        return {
            "id": response["id"],
            "partition_key": response.get("partition_key"),
            "etag": response.get("_etag"),
            "updated": True,
        }
    except CosmosAccessConditionFailedError:
        return {
            "id": document_id,
            "updated": False,
            "error": "ETag mismatch or document modified by another process",
        }
