import os
from boto3 import client
from botocore.client import Config
from typing import Optional


class StorageClient:
    """
    Client helper for Amazon S3 interactions.
    """

    def __init__(self):
        self.s3_client = client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
        )

    def get_client(self):
        """Returns the S3 client."""
        return self.s3_client


def load_config() -> dict:
    """
    Loads configuration for Amazon S3 from environment variables.

    Returns:
        Dictionary containing configuration (e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
    """
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
