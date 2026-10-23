# [HELPER] database_client.py
# Local configuration and helper utilities for Amazon DynamoDB NoSQL store

import os
import boto3
from botocore.exceptions import ClientError

# ---- Configuration ----------------------------------------------------------
# Load AWS credentials from environment variables (recommended for security)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

# ---- DynamoDB Client Factory ------------------------------------------------

ddb_client = boto3.client(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def get_table_resource(table_name):
    """Retrieve a DynamoDB Table resource object for fluent API usage."""
    return ddb_client.Table(table_name)


def dict_to_dynamodb(item_dict):
    """Convert a plain Python dict to a DynamoDB attribute dict."""
    return {k: {"S": str(v)} for k, v in item_dict.items()}


def dynamodb_to_dict(dynamodb_item):
    """Convert a DynamoDB attribute dict back to a normal Python dict."""
    return {k: v["S"] for k, v in dynamodb_item.items()}


# Example helper usage (uncomment to test locally)
# table = get_table_resource('my-table')
# item = dict_to_dynamodb({'name': 'Alice', 'age': 30})
# print(item)
