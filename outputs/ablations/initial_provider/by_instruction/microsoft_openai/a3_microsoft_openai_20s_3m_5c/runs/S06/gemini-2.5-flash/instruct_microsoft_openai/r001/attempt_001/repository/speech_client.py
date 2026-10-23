import os
from typing import Dict, Any

# This file can be used to define common configurations or client initialization logic
# for various Text-to-Speech providers, or general utility functions.

def get_aws_config() -> Dict[str, str]:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "region_name": os.environ.get("AWS_REGION", "us-east-1"),
    }

def get_openai_api_key() -> str:
    return os.environ.get("OPENAI_API_KEY", "")

def get_google_credentials_path() -> str:
    return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
