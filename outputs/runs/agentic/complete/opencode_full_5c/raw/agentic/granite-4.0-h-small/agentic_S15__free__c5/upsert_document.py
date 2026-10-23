# upsert_document.py
# Provider: AWS DynamoDB (Amazon Managed NoSQL Document Store)
import json
from boto3 import resource
from database_client import get_dynamodb_client


def upsert_document(identifier: str, document: dict) -> None:
    """Upsert a JSON document in DynamoDB by its primary identifier.

    Args:
        identifier (str): Primary key of the document.
        document (dict): The JSON document to upsert.
    """
    # load client with provider credentials via helper
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("Documents")  # replace with your table name
    response = table.put_item(Item=document)
    # response can be inspected for conditional errors if needed
