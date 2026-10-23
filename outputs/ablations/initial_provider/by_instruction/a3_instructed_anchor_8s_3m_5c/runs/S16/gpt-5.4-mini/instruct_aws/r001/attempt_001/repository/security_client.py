import os

import boto3


def load_secret_id(default_name: str) -> str:
    return os.environ.get("AWS_SECRET_ID", default_name)


def load_aws_region(default_region: str = "us-east-1") -> str:
    return os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", default_region))


def secrets_manager_client():
    return boto3.client("secretsmanager", region_name=load_aws_region())


def get_secret_string(secret_id: str, version_stage: str | None = None, version_id: str | None = None) -> str:
    client = secrets_manager_client()
    params = {"SecretId": secret_id}
    if version_stage:
        params["VersionStage"] = version_stage
    if version_id:
        params["VersionId"] = version_id
    response = client.get_secret_value(**params)
    return response.get("SecretString", "")


def get_secret_bytes(secret_id: str, version_stage: str | None = None, version_id: str | None = None) -> bytes:
    client = secrets_manager_client()
    params = {"SecretId": secret_id}
    if version_stage:
        params["VersionStage"] = version_stage
    if version_id:
        params["VersionId"] = version_id
    response = client.get_secret_value(**params)
    blob = response.get("SecretBinary")
    if blob is None:
        return response.get("SecretString", "").encode("utf-8")
    return blob if isinstance(blob, bytes) else bytes(blob)
