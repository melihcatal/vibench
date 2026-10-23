from typing import Any, List
from boto3.dynamodb.conditions import Attr
from database_client import get_table
from database_models import DocumentDict


def query_documents(table_name: str, field: str, value: Any) -> List[DocumentDict]:
    table = get_table(table_name)
    response = table.scan(FilterExpression=Attr(field).eq(value))
    return response.get("Items", [])
