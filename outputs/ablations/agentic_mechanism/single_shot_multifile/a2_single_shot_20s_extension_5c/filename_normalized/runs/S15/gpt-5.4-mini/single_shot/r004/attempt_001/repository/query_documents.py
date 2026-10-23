from typing import Any, Dict

from boto3.dynamodb.conditions import Attr, Key

from database_client import get_table
from database_models import QueryDocumentsRequest, document_from_item


def query_documents(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = QueryDocumentsRequest.from_dict(payload)
    table = get_table()
    if request.partition_key and request.partition_value is not None:
        response = table.query(KeyConditionExpression=Key(request.partition_key).eq(request.partition_value))
    elif request.field_name and request.field_value is not None:
        response = table.scan(FilterExpression=Attr(request.field_name).eq(request.field_value))
    else:
        response = table.scan()
    items = [document_from_item(item) for item in response.get("Items", [])]
    return {"items": items, "count": len(items)}
