import os
from typing import Dict, Any
from database_client import get_dynamodb_client, get_table_name, serialize_item
from database_models import Document

def upsert_document(document: Document) -> Dict[str, Any]:
    """
    Upserts a JSON document by its primary identifier into AWS DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    item_to_put = document.model_dump()
    
    dynamodb_item = serialize_item(item_to_put)
    
    response = dynamodb.put_item(
        TableName=table_name,
        Item=dynamodb_item
    )
    return response
