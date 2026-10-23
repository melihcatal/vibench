import os
from typing import Any, List
from boto3.dynamodb.conditions import Attr
from database_client import get_table
from database_models import QueryResponse

def query_documents(field: str, value: Any) -> QueryResponse:
    table = get_table()
    response = table.scan(
        FilterExpression=Attr(field).eq(value)
    )
    return response['Items']
