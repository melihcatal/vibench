import os
from typing import Optional, Dict, Any
from database_client import get_dynamodb_client, get_table_name, serialize_item, deserialize_item
from database_models import Document, FetchDocumentResponse

def fetch_document(document_id: str) -> Optional[Document]:
    """
    Fetches a document by identifier from AWS DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    key = {"id": document_id}
    dynamodb_key = serialize_item(key)

    response = dynamodb.get_item(
        TableName=table_name,
        Key=dynamodb_key
    )
    
    item = response.get("Item")
    if item:
        deserialized_item = deserialize_item(item)
        return Document(**deserialized_item)
    return None
