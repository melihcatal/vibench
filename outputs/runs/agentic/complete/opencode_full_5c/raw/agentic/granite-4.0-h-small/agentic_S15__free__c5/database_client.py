# database_client.py
# Local helper: Managed NoSQL Document Store client utilities
import os
from boto3 import client
from botocore.config import Config


def get_dynamodb_client() -> client:
    """Create and return a boto3 DynamoDB client with provider configuration.

    The helper abstracts credential retrieval and retry configuration.
    Environment variables or AWS config files can be used for credentials.
    """
    # Example: use default AWS credential chain (env, shared config, IAM role)
    config = Config(retries={"max_attempts": 10, "mode": "standard"})
    return client(
        "dynamodb",
        # Region can be overridden via env var or config file
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        config=config,
    )
