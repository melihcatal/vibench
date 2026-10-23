import os

from database_client import get_dynamodb_resource


def fetch_document(document_id: str, table_name: str, key_field: str = "id"):
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={key_field: document_id})
    return response.get("Item")
