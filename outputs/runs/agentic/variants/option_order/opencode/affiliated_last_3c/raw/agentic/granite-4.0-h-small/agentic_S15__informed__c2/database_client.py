import os
import boto3
from typing import Any, Dict


class DatabaseClient:
    """Local helper that centralises AWS credential handling and creates a boto3 DynamoDB client.

    The class provides a single instance method `get_dynamodb_client` which returns a ready-to-use
    DynamoDB resource. It reads credentials from environment variables which is the standard
    way to authenticate boto3 in managed environments.
    """

    @staticmethod
    def get_dynamodb_client() -> boto3.resource:
        """Return a boto3 DynamoDB resource configured with AWS credentials from environment.

        Expected environment variables:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION (optional, defaults to us-east-1)
        """
        region = os.getenv("AWS_REGION", "us-east-1")
        # boto3 automatically reads AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from env
        return boto3.resource("dynamodb", region_name=region)
