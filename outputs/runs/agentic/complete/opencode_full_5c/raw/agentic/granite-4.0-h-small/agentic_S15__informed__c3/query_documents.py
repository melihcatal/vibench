# [SAME-SCENARIO] query_documents.py
# Query documents in DynamoDB by a field value or partition-style key

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


def query_documents(
    table_name, key_condition_expr, expression_attribute_values=None, limit=None
):
    """Query a DynamoDB table.

    Args:
        table_name (str): Name of the DynamoDB table.
        key_condition_expr (str): Expression for the partition key filter, e.g. "#pk = :pk".
        expression_attribute_values (dict, optional): Mapping of placeholder names to values.
        limit (int, optional): Maximum number of items to return.

    Returns:
        list: List of matching documents (each a dict of attribute strings).
    """
    try:
        params = {"TableName": table_name, "KeyConditionExpression": key_condition_expr}
        if expression_attribute_values:
            params["ExpressionAttributeValues"] = expression_attribute_values
        if limit is not None:
            params["Limit"] = limit
        response = ddb.query(**params)
        items = response.get("Items", [])
        # Convert DynamoDB attributes to normal dicts with string values
        return [{k: v["S"] for k, v in item.items()} for item in items]
    except ClientError as e:
        print(f"Error querying documents: {e}")
        raise
