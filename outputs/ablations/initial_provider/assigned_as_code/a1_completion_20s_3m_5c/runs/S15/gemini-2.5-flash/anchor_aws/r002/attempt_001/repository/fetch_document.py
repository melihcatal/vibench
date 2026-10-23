import os

from database_client import get_dynamodb_resource


def fetch_document(document_id, table_name=None, key_field=None):
    table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
    key_field = key_field or os.environ.get("DYNAMODB_KEY_FIELD", "id")

    if not table_name:
        raise ValueError("DynamoDB table name not provided.")

    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={key_field: document_id})
    return response.get("Item")
