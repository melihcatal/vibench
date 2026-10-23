import os
from database_client import get_dynamodb_client
from database_models import denormalize_item

def upsert_document(table_name: str, document: dict) -> dict:
    """
    Upserts a JSON document into an AWS DynamoDB table.
    The document must contain a 'document_id' for the primary key.
    """
    dynamodb = get_dynamodb_client()

    if "document_id" not in document:
        raise ValueError("Document must contain a 'document_id' field.")

    item = denormalize_item(document)

    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response

