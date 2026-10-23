import os
from typing import Dict, Any


def get_aws_config() -> Dict[str, Any]:
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    }


def get_azure_vault_url() -> str:
    return os.getenv("AZURE_KEY_VAULT_URL")


def get_google_project() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT")
