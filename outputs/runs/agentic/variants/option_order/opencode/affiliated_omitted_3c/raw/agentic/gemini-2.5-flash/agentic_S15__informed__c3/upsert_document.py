import os
from database_client import get_dynamodb_resource
from typing import Dict, Any


def upsert_document(table_name: str, document: Dict[str, Any]):
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=document)
    return response
