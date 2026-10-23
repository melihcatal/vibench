import os
from typing import Dict, Any

# Example configuration using AWS credentials - replace with your own environment variables or IAM role.
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def get_table(table_name: str) -> Any:
    """Retrieve a DynamoDB table reference."""
    return dynamodb.Table(table_name)


def normalize_request(document: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize and prepare a document payload for DynamoDB."""
    # Remove None values and ensure keys are DynamoDB-ready (e.g., strings, numbers, lists, maps)
    cleaned = {k: v for k, v in document.items() if v is not None}
    return cleaned


def normalize_response(item: Dict[str, Any]) -> Dict[str, Any]:
    """Extract values from DynamoDB attribute map format."""
    # In boto3, .get('Item') returns raw attribute map; convert to plain dict if needed
    return item


def parse_error(error: Exception) -> str:
    """Convert DynamoDB client errors into a readable message."""
    return f"DynamoDB error: {error}"
