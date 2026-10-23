# [SAME-SCENARIO] fetch_document.py
import os
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

TABLE_NAME = os.getenv("DYNAMODB_TABLE", "Documents")

table = dynamodb.Table(TABLE_NAME)


def fetch_document(doc_id):
    """Retrieve a document from DynamoDB by its primary identifier.

    Args:
        doc_id (str): The identifier of the document.

    Returns:
        dict: The JSON document if found; None otherwise.
    """
    response = table.get_item(Key={"id": doc_id})
    return response.get("Item")
