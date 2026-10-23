import os
import boto3

# Load DynamoDB table name from env
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

ddb = boto3.resource("dynamodb")


def fetch_document(identifier):
    """Retrieve a document by its primary identifier from DynamoDB.

    Returns the document as a dict or None if not found.
    """
    table = ddb.Table(TABLE_NAME)
    try:
        response = table.get_item(Key={"id": identifier})
        if "Item" in response:
            return response["Item"]
        else:
            return None
    except Exception as e:
        raise RuntimeError(f"Error fetching document: {e}")
