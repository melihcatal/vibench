from typing import Any, Dict, List

from boto3.dynamodb.conditions import Attr, Key

from database_client import table_resource
from database_models import DocumentQueryRequest, DocumentQueryResponse


def query_documents(field_name: str, field_value: Any, index_name: str | None = None) -> Dict[str, Any]:
    request = DocumentQueryRequest(field_name=field_name, field_value=field_value, index_name=index_name)
    table = table_resource()
    if request.index_name:
        response = table.query(IndexName=request.index_name, KeyConditionExpression=Key(request.field_name).eq(request.field_value))
    else:
        response = table.scan(FilterExpression=Attr(request.field_name).eq(request.field_value))
    items = response.get("Items", [])
    result = DocumentQueryResponse(items=items, count=len(items))
    return {"count": result.count, "items": result.items}
