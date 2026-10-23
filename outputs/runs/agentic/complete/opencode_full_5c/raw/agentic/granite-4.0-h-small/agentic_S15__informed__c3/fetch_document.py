# [SAME-SCENARIO] fetch_document.py
# Retrieves a JSON document by its primary identifier from Amazon DynamoDB

import os
import json
import boto3
from botocore.exceptions import ClientError

# Configure the DynamoDB client using environment variables for authentication
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

ddb = boto3.client(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def fetch_document(table_name, primary_key):
    """Fetch a document by its primary key from DynamoDB.

    Args:
        table_name (str): Name of the DynamoDB table.
        primary_key (str): The document's primary identifier (partition key).

    Returns:
        dict: JSON document as a Python dict, or None if not found.
    """
    try:
        response = ddb.get_item(
            TableName=table_name, Key={"id": {"S": str(primary_key)}}
        )
        item = response.get("Item")
        if item:
            # Convert DynamoDB attribute values back to native types
            return {k: v["S"] for k, v in item.items()}
        return None
    except ClientError as e:
        print(f"Error fetching document: {e}")
        raise
