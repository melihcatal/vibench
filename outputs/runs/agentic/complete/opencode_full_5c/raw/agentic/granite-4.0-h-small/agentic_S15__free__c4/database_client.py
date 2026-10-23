# [HELPER] database_client.py
"""Local helper to configure and provide a DynamoDB client for NoSQL document store integrations.

This module loads AWS credentials and region from environment variables and provides
reusable client instances via the `get_dynamodb_client` function.
"""

import os
import boto3
from botocore.config import Config


def get_dynamodb_client() -> boto3.client:
    """Return a shared DynamoDB client configured for the current environment.

    Uses standard AWS SDK mechanisms: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN (optional), and AWS_REGION.
    """
    # Optional: configure retries and timeouts to improve reliability
    custom_config = Config(
        retries={"max_attempts": 5, "mode": "adaptive"},
        read_timeout=10,
        connect_timeout=5,
    )
    return boto3.client(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        config=custom_config,
    )
