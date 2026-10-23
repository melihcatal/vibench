# conditional_update.py
"""
Same-scenario implementation file.

Applies a conditional (version-aware) update to a stored JSON document in DynamoDB.
Ensures the update only succeeds if the document version matches the expected value.
Provider identifiable in code: boto3 DynamoDB client and UpdateItem with ConditionExpression.
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
VERSION_FIELD = os.getenv("VERSION_FIELD", "version")


def conditional_update(doc_id, update_fields, expected_version):
    """Update fields of a document only if its current version matches expected_version.

    Args:
        doc_id (str): The primary identifier (partition key).
        update_fields (dict): Fields to set or modify.
        expected_version (int): The version value that must be present for the update to proceed.

    Returns:
        dict: DynamoDB response containing attributes and consumed capacity.
    """
    table = dynamodb.Table(TABLE_NAME)
    response = table.update_item(
        Key={PRIMARY_KEY_NAME: doc_id},
        UpdateExpression="SET #n = :new, #v = #v + :inc",
        ConditionExpression=f"#v = :expected",
        ExpressionAttributeNames={"#n": next(iter(update_fields)), "#v": VERSION_FIELD},
        ExpressionAttributeValues={
            ":new": update_fields[next(iter(update_fields))],
            ":inc": 1,  # increment version by 1
            ":expected": expected_version,
        },
        ReturnValues="ALL_NEW",
    )
    return response
