from typing import Any, Dict
from database_client import DatabaseClient
from database_models import DocumentRequest, normalize_document


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Upsert a JSON document into Azure Cosmos DB by its primary identifier."""
    client = DatabaseClient().get_container()
    request = DocumentRequest(**document)
    normalized = normalize_document(
        {
            "id": request.document_id,
            "partition_key": request.partition_key,
            "body": request.body,
        }
    )

    response = client.upsert_item(normalized)
    return {
        "id": response["id"],
        "partition_key": response.get("partition_key"),
        "etag": response.get("_etag"),
    }
