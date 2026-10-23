from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import get_table, serialize_item
from database_models import DocumentRequest, DocumentResponse

PROVIDER_NAME = "Amazon DynamoDB"
PROVIDER_SDK = "boto3"


def upsert_document(document: Dict[str, Any], table_name: Optional[str] = None, primary_key: str = "id") -> Dict[str, Any]:
    request = DocumentRequest(document=document, primary_key=primary_key)
    item = serialize_item(request.normalized())
    table = get_table(table_name)
    table.put_item(Item=item)
    return DocumentResponse(document=item, source=PROVIDER_NAME.lower().replace(" ", "-")).as_dict()
