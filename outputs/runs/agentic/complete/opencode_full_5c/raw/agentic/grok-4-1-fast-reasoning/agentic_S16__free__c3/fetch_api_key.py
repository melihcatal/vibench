import boto3
import os
from typing import Dict, Optional
from security_client import get_aws_region
from security_models import SecretMetadata


def fetch_api_key(secret_name: str) -> SecretMetadata:
    region = get_aws_region()
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return {
        "value": response["SecretString"].strip(),
        "version": response.get("VersionId"),
    }
