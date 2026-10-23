from database_client import get_dynamodb_client
from database_models import normalize_item, denormalize_item

def fetch_document(table_name: str, document_id: str) -> dict:
    """
    Fetches a document by its primary identifier from an AWS DynamoDB table.
    """
    dynamodb = get_dynamodb_client()

    key = denormalize_item({"document_id": document_id})

    response = dynamodb.get_item(
        TableName=table_name,
        Key=key
    )

    item = response.get("Item")
    return normalize_item(item) if item else {}
