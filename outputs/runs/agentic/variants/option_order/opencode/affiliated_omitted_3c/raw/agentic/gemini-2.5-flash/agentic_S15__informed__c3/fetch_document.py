import os
from database_client import get_dynamodb_resource
from typing import Dict, Any


def fetch_document(table_name: str, key: Dict[str, Any]):
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get("Item")
