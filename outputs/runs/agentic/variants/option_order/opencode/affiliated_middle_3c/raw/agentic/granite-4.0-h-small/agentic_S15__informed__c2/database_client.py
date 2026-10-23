# database_client.py
"""
Local helper file.

Provides local configuration, client initialization and helper utilities for the Managed NoSQL Document Store.
Concrete provider used: Amazon DynamoDB via boto3.
"""

import json
import os
from boto3 import client as boto3_client

# Provider credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME", "us-east-1")

# Initialize the DynamoDB client
dynamodb = boto3_client(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

# Configuration constants (read from env or defaults)
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
if not TABLE_NAME:
    raise RuntimeError("Environment variable DYNAMODB_TABLE_NAME must be set")
PRIMARY_KEY_NAME = os.getenv("DYNAMODB_PRIMARY_KEY", "id")


def normalize_document(doc: dict) -> dict:
    """
    Normalizes a document read from DynamoDB, e.g., converts binary to base64.

    Args:
        doc (dict): Raw DynamoDB item dictionary.

    Returns:
        dict: Normalized plain‑Python document.
    """
    normalized = dict(doc)
    for key, value in doc.items():
        if isinstance(value, dict) and "B" in value:
            normalized[key] = value["B"]
    return normalized
