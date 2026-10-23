import os
from typing import Any, Dict
from database_client import DatabaseClient
from database_models import DocumentRequest, normalize_document


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Upserts a JSON document into Azure Cosmos DB by its primary identifier."""
    client = DatabaseClient()
    container = client.get_container()

    normalized_doc = normalize_document(document)
    request: DocumentRequest = {
        "id": normalized_doc["id"],
        "partition_key": normalized_doc.get("partition_key", normalized_doc["id"]),
        "body": normalized_doc,
    }

    try:
        response = container.upsert_item(body=request["body"])
        return {
            "id": response["id"],
            "status": "upserted",
            "etag": response.get("_etag"),
        }
    except Exception as e:
        raise Exception(f"Failed to upsert document: {str(e)}")
