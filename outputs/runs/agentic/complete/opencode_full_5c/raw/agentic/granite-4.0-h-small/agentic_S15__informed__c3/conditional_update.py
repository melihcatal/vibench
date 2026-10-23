# [SAME-SCENARIO] conditional_update.py
# Apply a version-aware conditional update to a document in DynamoDB

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


def conditional_update(
    table_name, primary_key, update_expression, condition_expression
):
    """Perform a conditional update on a DynamoDB item.

    The update only succeeds if the condition expression evaluates to true,
    typically used to enforce version numbers or existence checks.

    Args:
        table_name (str): Name of the DynamoDB table.
        primary_key (str): The document's primary identifier (partition key).
        update_expression (str): DynamoDB UpdateExpression, e.g. "SET #v = :v".
        condition_expression (str): DynamoDB ConditionExpression for version check.

    Returns:
        dict: Response from DynamoDB, or None if the condition was not met.
    """
    try:
        response = ddb.update_item(
            TableName=table_name,
            Key={"id": {"S": str(primary_key)}},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ReturnValues="ALL_NEW",
        )
        # Convert and return the updated item
        item = response.get("Attributes", {})
        return {k: v["S"] for k, v in item.items()}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # No update performed because condition failed
            return None
        print(f"Conditional update error: {e}")
        raise
