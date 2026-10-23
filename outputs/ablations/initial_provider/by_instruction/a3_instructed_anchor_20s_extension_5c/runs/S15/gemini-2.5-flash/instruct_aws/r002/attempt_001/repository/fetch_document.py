import os
from database_client import get_dynamodb_client
from database_models import Document

def fetch_document(table_name: str, document_id: str) -> Document | None:
    """
    Fetches a document by its identifier from an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        document_id: The primary identifier of the document.

    Returns:
        The Document object if found, otherwise None.
    """
    dynamodb = get_dynamodb_client()

    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            "document_id": {"S": document_id}
        }
    )

    item = response.get("Item")
    if item:
        return Document.from_item(item)
    return None
