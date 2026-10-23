from typing import Dict, Any
from database_client import DatabaseClient
from database_models import DocumentRequest, normalize_document


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Upsert a document into Azure Cosmos DB NoSQL store."""
    client = DatabaseClient().get_container()
    request = DocumentRequest(**document)

    document["id"] = request.document_id
    document["partition_key"] = request.partition_key

    response = client.upsert_item(body=document)
    return normalize_document(response).dict()
