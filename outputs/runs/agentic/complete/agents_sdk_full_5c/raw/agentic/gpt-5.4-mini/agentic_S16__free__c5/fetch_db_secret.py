import os
from typing import Optional

from security_client import get_secret_manager_client, get_secret_name
from security_models import SecretFetchRequest, parse_json_or_string_secret

# AWS Secrets Manager integration
import boto3


def fetch_db_secret(version: str = "AWSCURRENT", secret_id: Optional[str] = None, region_name: Optional[str] = None):
    region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    secret_name = get_secret_name(None, secret_id or os.getenv("DB_SECRET_ID", "database/connection"))
    client = get_secret_manager_client(provider="aws", region_name=region)
    request = SecretFetchRequest(secret_name=secret_name, version=version)
    response = client.get_secret_value(SecretId=request.secret_name, VersionStage=request.version)
    secret_string = response.get("SecretString") or response.get("SecretBinary", b"")
    return parse_json_or_string_secret(secret_string)
