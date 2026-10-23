# upsert_document.py
"""
Same-scenario integration file for upserting a JSON document into a managed NoSQL document store.
Provider: Amazon DynamoDB (via boto3 SDK).
"""

import json
import boto3
from database_client import NoSQLClient


def upsert_document(identifier, document):
    """Upsert a JSON document in the NoSQL store using its primary identifier.

    Args:
        identifier (str): The primary key of the document.
        document (dict): The JSON document to upsert.
    """
    client = NoSQLClient()
    table_name = client.config["TABLE_NAME"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    # Use PutItem which creates or replaces the item
    response = table.put_item(Item={**document, client.partition_key: identifier})
    return response
