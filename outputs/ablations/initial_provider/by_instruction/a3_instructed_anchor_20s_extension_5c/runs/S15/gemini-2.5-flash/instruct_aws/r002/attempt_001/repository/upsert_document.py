import os
from database_client import get_dynamodb_client
from database_models import Document

def upsert_document(table_name: str, document: Document) -> dict:
    """
    Upserts a JSON document into an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        document: The Document object to upsert.

    Returns:
        A dictionary containing the response from DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    item = document.to_item()
    
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response
