from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import DocumentQueryRequest


def query_documents(request: DocumentQueryRequest):
    table = get_table()
    response = table.scan(
        FilterExpression=Attr(request.field_name).eq(request.field_value)
    )
    return response.get("Items", [])
