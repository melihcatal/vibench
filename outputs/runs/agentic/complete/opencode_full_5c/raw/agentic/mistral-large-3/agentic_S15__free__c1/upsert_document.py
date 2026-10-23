from typing import Any, Dict
from database_client import DatabaseClient
from database_models import DocumentRequest, normalize_document


def upsert_document(request: DocumentRequest) -> Dict[str, Any]:
    client = DatabaseClient().get_container()
    document = normalize_document(request["document"])
    document["id"] = request["id"]
    document["partition_key"] = request["partition_key"]

    response = client.upsert_item(body=document)
    return {
        "id": response["id"],
        "partition_key": response["partition_key"],
        "etag": response["_etag"],
    }
