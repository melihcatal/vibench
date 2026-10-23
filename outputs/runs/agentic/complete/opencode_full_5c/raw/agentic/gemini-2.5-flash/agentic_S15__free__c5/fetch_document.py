from database_client import get_dynamodb_client
from database_models import Document
import os


def fetch_document(document_id: str) -> Document | None:
    """
    Fetches a document by identifier from AWS DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get(
        "DYNAMODB_TABLE_NAME", "your-document-table"
    )  # AWS DynamoDB

    response = dynamodb.get_item(TableName=table_name, Key={"id": {"S": document_id}})

    item = response.get("Item")
    if item:
        return Document.from_dynamodb_item(item)
    return None
