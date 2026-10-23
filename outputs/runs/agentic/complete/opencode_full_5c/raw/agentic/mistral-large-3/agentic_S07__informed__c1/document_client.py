import os
from typing import Dict, Optional
import boto3
from botocore.config import Config


def get_document_client(service: str):
    """
    Provides a configured client for Amazon Textract.
    """
    if service == "textract":
        return boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            config=Config(retries={"max_attempts": 3}),
        )
    raise ValueError(f"Unsupported service: {service}")
