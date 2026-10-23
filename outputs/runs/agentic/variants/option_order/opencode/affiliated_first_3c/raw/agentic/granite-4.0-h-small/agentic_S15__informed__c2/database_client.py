import os
import json
import boto3
from boto3.dynamodb.conditions import Attr

# DynamoDB configuration via environment variables
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

ddb = boto3.resource("dynamodb", region_name=AWS_REGION)


def get_table():
    """Return the DynamoDB table instance."""
    return ddb.Table(TABLE_NAME)


def put_item(item):
    """Helper to put an item (upsert) into the table."""
    table = get_table()
    return table.put_item(Item=item)


def get_item(key):
    """Retrieve an item by its primary key."""
    table = get_table()
    response = table.get_item(Key=key)
    return response.get("Item")


def query_items(partition_key, filter_expr=None):
    """Query items with a partition key condition and optional filter expression."""
    table = get_table()
    key_condition = Attr(partition_key).eq(os.getenv(partition_key))
    kwargs = {"KeyConditionExpression": key_condition}
    if filter_expr:
        kwargs["FilterExpression"] = filter_expr
    results = table.query(**kwargs)
    return results.get("Items", [])
