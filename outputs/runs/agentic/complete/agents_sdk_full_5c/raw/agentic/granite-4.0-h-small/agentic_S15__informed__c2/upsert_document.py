import os
import json
from database_client import get_dynamodb_client
from database_models import Document

def upsert_document(identifier: str, document_dict: dict):
    """Upsert a JSON document into DynamoDB using its primary identifier.

    Args:
        identifier (str): The partition key value for the document.
        document_dict (dict): The JSON document data.
    """
    client = get_dynamodb_client()
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RuntimeError("DYNAMODB_TABLE_NAME environment variable not set")

    # Normalize document using local helper
    doc = Document.from_dict(document_dict)

    # Use DynamoDB's PutItem which creates or replaces the item
    response = client.put_item(
        TableName=table_name,
        Item=json.loads(doc.to_dynamodb_json())
    )
    print(f"Upserted document {identifier}: {response}")
