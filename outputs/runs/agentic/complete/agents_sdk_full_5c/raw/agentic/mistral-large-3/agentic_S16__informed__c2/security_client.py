import os
from typing import Optional

def get_vault_url() -> str:
    return os.getenv("AZURE_KEY_VAULT_URL", "")

def get_aws_credentials() -> dict:
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.getenv("AWS_REGION", "us-east-1")
    }

def get_google_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_PROJECT_ID")