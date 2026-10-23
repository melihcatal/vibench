# database_client.py
"""
Local helper file providing configuration and client utilities for the Managed NoSQL Document Store.
Uses environment variables to load credentials and endpoint configuration for Amazon DynamoDB.
"""

import os
import boto3
from botocore.config import Config


class NoSQLClient:
    """Singleton-like client helper for DynamoDB operations."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = cls._create()
        return cls._instance

    @staticmethod
    def _create():
        region = os.getenv("DYNAMODB_REGION", "us-east-1")
        endpoint_url = os.getenv(
            "DYNAMODB_ENDPOINT"
        )  # optional for local emulator (e.g., DynamoDB Local)
        config = Config(retries={"max_attempts": 5, "mode": "standard"})
        session = boto3.Session(region_name=region)
        dynamodb = session.resource(
            "dynamodb", endpoint_url=endpoint_url, config=config
        )
        # Configuration shared across helper functions
        config = {
            "TABLE_NAME": os.getenv("DYNAMODB_TABLE", "documents"),
            "PARTITION_KEY": os.getenv("DYNAMODB_PARTITION_KEY", "id"),
        }
        # Expose both the dynamodb resource and shared config
        return type("NoSQLClient", (), {"resource": dynamodb, "config": config})()
