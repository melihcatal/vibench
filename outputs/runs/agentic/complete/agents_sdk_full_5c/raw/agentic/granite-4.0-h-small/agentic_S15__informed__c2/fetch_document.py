import os
from database_client import get_dynamodb_client
from database_models import Document

def fetch_document(identifier: str):
    """Retrieve a JSON document from DynamoDB by its primary identifier.

    Args:
        identifier (str): The partition key value for the document.

    Returns:
        dict: The deserialized document data.
    """
    client = get_dynamodb_client()
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RuntimeError("DYNAMODB_TABLE_NAME environment variable not set")

    response = client.get_item(
        TableName=table_name,
        Key={"id": {"S": identifier}}
    )
    item = response.get("Item")
    if not item:
        raise KeyError(f"Document with id {identifier} not found")
    # Convert DynamoDB dict to normal dict and then to Document
    doc = Document.from_dynamodb_map(item)
    return doc.to_dict()
