from boto3.dynamodb.conditions import Attr

from database_client import document_table
from database_models import DocumentResponse, QueryDocumentsRequest


def query_documents(field_name, field_value):
    table = document_table()
    response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    items = response.get("Items", [])
    return DocumentResponse(
        ok=True, data={"documents": items, "count": len(items)}
    ).__dict__


def handler(event, context=None):
    req = QueryDocumentsRequest(
        field_name=event.get("field_name"), field_value=event.get("field_value")
    )
    return query_documents(req.field_name, req.field_value)
