import base64
import os
from typing import Optional

import boto3


def read_secret_version(secret_id: Optional[str] = None, version_id: Optional[str] = None, version_stage: Optional[str] = None, region_name: Optional[str] = None) -> str:
    secret_id = secret_id or os.environ.get("AWS_SECRET_NAME") or os.environ.get("SECRET_ID")
    if not secret_id:
        raise ValueError("Missing secret id; set AWS_SECRET_NAME or SECRET_ID")
    region = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("secretsmanager", region_name=region)
    kwargs = {"SecretId": secret_id}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage
    response = client.get_secret_value(**kwargs)
    secret_string = response.get("SecretString")
    if isinstance(secret_string, str) and secret_string:
        return secret_string
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret value is empty")
    if isinstance(secret_binary, bytes):
        return secret_binary.decode("utf-8")
    return base64.b64decode(secret_binary).decode("utf-8")


def read_staged_secret(secret_id: Optional[str] = None, stage: Optional[str] = None, region_name: Optional[str] = None) -> str:
    return read_secret_version(secret_id=secret_id, version_stage=stage or "AWSCURRENT", region_name=region_name)
