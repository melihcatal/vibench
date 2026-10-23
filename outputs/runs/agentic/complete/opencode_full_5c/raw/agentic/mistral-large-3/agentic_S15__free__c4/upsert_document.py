from typing import Any, Dict
from database_client import DatabaseClient
from database_models import DocumentRequest, normalize_document


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    client = DatabaseClient().get_container()
    document_request = DocumentRequest(**document)

    cosmos_document = {
        "id": document_request.document_id,
        "partitionKey": document_request.partition_key,
        **document_request.document_data,
    }

    response = client.upsert_item(body=cosmos_document)
    return normalize_document(response).dict(by_alias=True)
