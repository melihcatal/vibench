from database_client import get_dynamodb_table
from database_models import documents_from_items, Document
from boto3.dynamodb.conditions import Attr

def query_documents(field: str, value: str) -> list[Document]:
    table = get_dynamodb_table()
    response = table.scan(
        FilterExpression=Attr(field).eq(value)
    )
    return documents_from_items(response['Items'])
