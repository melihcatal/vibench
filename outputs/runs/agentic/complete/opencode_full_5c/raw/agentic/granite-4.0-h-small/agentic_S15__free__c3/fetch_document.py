# fetch_document.py
"""
Same-scenario integration file for fetching a JSON document from a managed NoSQL document store.
Provider: Amazon DynamoDB (via boto3 SDK).
"""

import boto3
from database_client import NoSQLClient


def fetch_document(identifier):
    """Retrieve a document by its primary identifier.

    Args:
        identifier (str): The partition key (primary key) for the document.

    Returns:
        dict: The fetched document, or None if not found.
    """
    client = NoSQLClient()
    table_name = client.config["TABLE_NAME"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={client.partition_key: identifier})
    item = response.get("Item")
    return item
