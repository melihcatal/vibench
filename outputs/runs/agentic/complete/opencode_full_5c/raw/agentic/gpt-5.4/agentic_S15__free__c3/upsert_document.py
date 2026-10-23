from typing import Any, Dict

from database_client import get_cosmos_container
from database_models import UpsertRequest, build_document_result


def upsert_document(
    document: Any, document_id: Any = None, partition_key: Any = None
) -> Dict[str, Any]:
    request = UpsertRequest.create(
        document=document, document_id=document_id, partition_key=partition_key
    )
    container = get_cosmos_container()
    response = container.upsert_item(body=request.document)
    result = build_document_result(
        response, headers=response.get("_response_headers", {})
    )
    return {
        "provider": "azure-cosmos-db",
        "found": result.found,
        "document": result.document,
        "etag": response.get("_etag"),
        "id": request.document["id"],
        "partitionKey": request.document["partitionKey"],
    }
