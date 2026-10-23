# fetch_document.py
# Provider: AWS DynamoDB (Amazon Managed NoSQL Document Store)
from boto3 import resource
from database_client import get_dynamodb_client


def fetch_document(identifier: str) -> dict:
    """Fetch a document from DynamoDB by its primary identifier.

    Args:
        identifier (str): Primary key of the document.

    Returns:
        dict: The stored JSON document.
    """
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("Documents")
    response = table.get_item(Key={"id": identifier})
    item = response.get("Item")
    return item or {}
