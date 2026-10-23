import os

# Local configuration utilities for OCR / layout services
# Provider selection is done via environment variables (example with Amazon Textract)


def get_aws_credentials() -> dict:
    """Return AWS credentials read from environment."""
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }


# Helper to build Textract client with credentials


def create_textract_client() -> object:
    """Create and return a configured boto3 Textract client."""
    creds = get_aws_credentials()
    return boto3.client("textract", **creds)


# Generic placeholder for other providers (e.g., Alibaba, Google) can be added similarly
