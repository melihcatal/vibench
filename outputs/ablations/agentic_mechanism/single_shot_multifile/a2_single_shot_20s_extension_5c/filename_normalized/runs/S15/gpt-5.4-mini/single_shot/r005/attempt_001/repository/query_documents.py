from typing import Any, Dict
from boto3.dynamodb.conditions import Attr, Key
from database_client import get_dynamodb_table
from database_models import DocumentQueryRequest, DocumentQueryResponse, normalize_document


def query_documents(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = DocumentQueryRequest.from_dict(payload)
    table = get_dynamodb_table()
    if request.index_name:
        response = table.query(
            IndexName=request.index_name,
            KeyConditionExpression=Key(request.field_name).eq(request.field_value),
        )
    else:
        response = table.scan(FilterExpression=Attr(request.field_name).eq(request.field_value))
    items = [normalize_document(item) for item in response.get("Items", [])]
    return DocumentQueryResponse(ok=True, items=items, count=len(items)).to_dict()


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return query_documents(event)
