from __future__ import annotations

from typing import Any, Dict, List, Optional

from boto3.dynamodb.conditions import Attr, Key

from database_client import get_table
from database_models import QueryRequest, QueryResponse

PROVIDER_NAME = "Amazon DynamoDB"
PROVIDER_SDK = "boto3"


def query_documents(field_name: str, field_value: Any, table_name: Optional[str] = None, limit: int = 50) -> Dict[str, Any]:
    request = QueryRequest(field_name=field_name, field_value=field_value, limit=limit)
    table = get_table(table_name)
    if field_name == "partition_key":
        result = table.query(KeyConditionExpression=Key(field_name).eq(request.field_value), Limit=request.limit)
    else:
        result = table.scan(FilterExpression=Attr(field_name).eq(request.field_value), Limit=request.limit)
    documents: List[Dict[str, Any]] = result.get("Items", [])
    return QueryResponse(documents=documents, source=PROVIDER_NAME.lower().replace(" ", "-")).__dict__
