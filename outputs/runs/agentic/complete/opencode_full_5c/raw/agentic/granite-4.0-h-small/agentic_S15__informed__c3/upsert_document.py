# [SAME-SCENARIO] upsert_document.py
# upserts a JSON document by its primary identifier using Amazon DynamoDB

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


def upsert_document(table_name, primary_key, document):
    """Insert or replace a document in DynamoDB.

    Args:
        table_name (str): Name of the DynamoDB table.
        primary_key (str): The document's primary identifier (partition key).
        document (dict): JSON‑serializable document to store.
    """
    try:
        # Use PutItem to create or replace the item
        response = ddb.put_item(
            TableName=table_name,
            Item={
                "id": {"S": str(primary_key)},
                **{k: {"S": str(v)} for k, v in document.items()},
            },
        )
        return response
    except ClientError as e:
        print(f"Error upserting document: {e}")
        raise
