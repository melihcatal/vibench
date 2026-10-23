import os
from typing import Any, Dict

from boto3.dynamodb.types import TypeSerializer

from database_client import document_key, table_resource
from database_models import DocumentUpsertRequest

serializer = TypeSerializer()


def upsert_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = DocumentUpsertRequest(
        document_id=str(payload["document_id"]),
        document=dict(payload.get("document", payload)),
        sort_key=payload.get("sort_key"),
    )
    item = request.to_item()
    item.update(document_key(request.document_id, request.sort_key))
    table_resource().put_item(Item={k: serializer.serialize(v) and v for k, v in item.items()})
    return {"status": "upserted", "document_id": request.document_id}
