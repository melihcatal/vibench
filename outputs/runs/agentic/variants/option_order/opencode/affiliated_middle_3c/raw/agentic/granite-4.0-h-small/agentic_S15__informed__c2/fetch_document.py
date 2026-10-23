# fetch_document.py
"""
Same-scenario implementation file.

Fetches a JSON document from a managed NoSQL document store by its identifier.
Provider identifiable in code: boto3 DynamoDB client and GetItem call.
"""

import json
import os
from boto3 import client as boto3_client

# Provider-specific configuration (credentials via environment variables)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME", "us-east-1")

# Initialise the DynamoDB client
dynamodb = boto3_client(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

# Constants
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
if not TABLE_NAME:
    raise RuntimeError("Environment variable DYNAMODB_TABLE_NAME must be set")

PRIMARY_KEY_NAME = os.getenv("DYNAMODB_PRIMARY_KEY", "id")


def fetch_document(doc_id):
    """Retrieve a JSON document by its primary identifier.

    Args:
        doc_id (str): The primary identifier (partition key).

    Returns:
        dict: The retrieved JSON document.
    """
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={PRIMARY_KEY_NAME: doc_id})
    item = response.get("Item")
    if not item:
        raise KeyError(f"Document with id {doc_id} not found")
    return item
