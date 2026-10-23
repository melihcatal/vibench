from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import get_table
from database_models import DocumentResponse

PROVIDER_NAME = "Amazon DynamoDB"
PROVIDER_SDK = "boto3"


def fetch_document(document_id: str, table_name: Optional[str] = None, primary_key: str = "id") -> Dict[str, Any]:
    table = get_table(table_name)
    response = table.get_item(Key={primary_key: str(document_id)})
    item = response.get("Item", {})
    return DocumentResponse(document=item, source=PROVIDER_NAME.lower().replace(" ", "-")).as_dict()
