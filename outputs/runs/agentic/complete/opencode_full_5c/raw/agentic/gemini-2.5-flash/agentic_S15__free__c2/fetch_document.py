from database_client import get_dynamodb_client
from database_models import Document
from typing import Dict, Any, Optional
import os


def fetch_document(
    document_id: str, table_name: str | None = None
) -> Optional[Dict[str, Any]]:
    """
    Fetches a document by its primary identifier from an AWS DynamoDB table.

    Args:
        document_id: The primary identifier of the document.
        table_name: The name of the DynamoDB table. Defaults to 'DocumentsTable'.

    Returns:
        The document data as a dictionary, or None if not found.
    """
    if table_name is None:
        table_name = os.getenv("DYNAMODB_TABLE_NAME", "DocumentsTable")

    dynamodb = get_dynamodb_client()

    response = dynamodb.get_item(TableName=table_name, Key={"id": {"S": document_id}})

    item = response.get("Item")
    if item:
        document = Document.from_dynamodb_item(item)
        if document:
            return {**{"id": document.document_id}, **document.data}
    return None
