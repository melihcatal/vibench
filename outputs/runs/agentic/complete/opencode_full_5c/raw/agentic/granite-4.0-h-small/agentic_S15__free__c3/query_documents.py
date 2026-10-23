# query_documents.py
"""
Same-scenario integration file for querying documents in a managed NoSQL document store.
Provider: Amazon DynamoDB (via boto3 SDK) using Query API.
"""

import boto3
from database_client import NoSQLClient


def query_documents(field_name, field_value):
    """Query documents where a given field matches the supplied value.

    Args:
        field_name (str): The attribute name to filter on.
        field_value (Any): The value to match.

    Returns:
        list[dict]: A list of matching documents.
    """
    client = NoSQLClient()
    table_name = client.config["TABLE_NAME"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    # Simple filter using KeyConditionExpression (if field is a partition/sort key) or Scan for attribute filtering
    if field_name == client.partition_key:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key(field_name).eq(
                field_value
            )
        )
    else:
        # Use Scan for non-key attribute filtering
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr(field_name).eq(field_value)
        )
    items = response.get("Items", [])
    return items
