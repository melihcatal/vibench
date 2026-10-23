from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import DocumentResponse


def query_documents(field_name, field_value):
    response = get_table().scan(FilterExpression=Attr(field_name).eq(field_value))
    documents = response.get("Items", [])
    return DocumentResponse(ok=True, documents=documents, message="queried")
