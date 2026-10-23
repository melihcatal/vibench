import os
from database_client import get_dynamodb_client
from database_models import DocumentKey


def fetch_document(table_name: str, key: DocumentKey):
    dynamodb = get_dynamodb_client()
    response = dynamodb.get_item(
        TableName=table_name, Key=key.model_dump(by_alias=True)
    )
    return response.get("Item")
