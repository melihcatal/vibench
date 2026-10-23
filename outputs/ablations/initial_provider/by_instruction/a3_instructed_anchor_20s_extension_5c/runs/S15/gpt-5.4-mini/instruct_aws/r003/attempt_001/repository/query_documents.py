from typing import Any, Dict, List

from boto3.dynamodb.conditions import Attr, Key

from database_client import documents_table
from database_models import QueryResponse, normalize_key


def query_documents(field_name: str, field_value: Any) -> QueryResponse:
    table = documents_table()
    if field_name == "id":
        response = table.query(KeyConditionExpression=Key("id").eq(normalize_key(field_value)))
    else:
        response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return QueryResponse(items=response.get("Items", []))
