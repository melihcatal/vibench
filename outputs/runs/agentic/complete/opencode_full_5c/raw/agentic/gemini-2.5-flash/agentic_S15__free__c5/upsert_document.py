from database_client import get_dynamodb_client
from database_models import Document
import os


def upsert_document(document: Document):
    """
    Upserts a JSON document by its primary identifier into AWS DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get(
        "DYNAMODB_TABLE_NAME", "your-document-table"
    )  # AWS DynamoDB

    item = document.to_dynamodb_item()

    response = dynamodb.put_item(TableName=table_name, Item=item)
    return response
