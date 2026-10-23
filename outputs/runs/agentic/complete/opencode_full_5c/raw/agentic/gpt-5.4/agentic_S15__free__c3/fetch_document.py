from typing import Any, Dict

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_cosmos_container
from database_models import DocumentRequest, build_document_result


def fetch_document(document_id: Any, partition_key: Any = None) -> Dict[str, Any]:
    request = DocumentRequest.create(
        document_id=document_id, partition_key=partition_key
    )
    container = get_cosmos_container()
    try:
        response = container.read_item(
            item=request.document_id, partition_key=request.partition_key
        )
    except CosmosResourceNotFoundError:
        result = build_document_result(None)
        return {
            "provider": "azure-cosmos-db",
            "found": result.found,
            "document": None,
            "etag": None,
        }
    result = build_document_result(
        response, headers=response.get("_response_headers", {})
    )
    return {
        "provider": "azure-cosmos-db",
        "found": result.found,
        "document": result.document,
        "etag": response.get("_etag"),
    }
