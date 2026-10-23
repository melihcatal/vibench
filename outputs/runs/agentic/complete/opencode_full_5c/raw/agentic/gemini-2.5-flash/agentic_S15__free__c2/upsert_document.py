from database_client import get_dynamodb_client
from database_models import Document
from typing import Dict, Any
import os


def upsert_document(
    document_id: str, document_data: Dict[str, Any], table_name: str | None = None
) -> Dict[str, Any]:
    """
    Upserts a JSON document into an AWS DynamoDB table.

    Args:
        document_id: The primary identifier for the document.
        document_data: The JSON data of the document.
        table_name: The name of the DynamoDB table. Defaults to 'DocumentsTable'.

    Returns:
        A dictionary containing the response from the DynamoDB put_item operation.
    """
    if table_name is None:
        table_name = os.getenv("DYNAMODB_TABLE_NAME", "DocumentsTable")

    dynamodb = get_dynamodb_client()

    # Create a Document object and convert it to DynamoDB item format
    document = Document(document_id, document_data)
    item = document.to_dynamodb_item()

    response = dynamodb.put_item(TableName=table_name, Item=item)
    return response
