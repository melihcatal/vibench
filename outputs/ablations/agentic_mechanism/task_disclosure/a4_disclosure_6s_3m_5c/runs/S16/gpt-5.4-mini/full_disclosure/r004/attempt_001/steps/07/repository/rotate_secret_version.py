import os
from typing import Optional

import boto3


def _secret_id() -> str:
    secret_id = os.environ.get("AWS_SECRET_ID") or os.environ.get("SECRET_ID")
    if not secret_id:
        raise ValueError("AWS_SECRET_ID or SECRET_ID is required")
    return secret_id


def _version_id() -> Optional[str]:
    return os.environ.get("AWS_SECRET_VERSION_ID") or os.environ.get("SECRET_VERSION_ID")


def _version_stage() -> Optional[str]:
    return os.environ.get("AWS_SECRET_VERSION_STAGE") or os.environ.get("SECRET_VERSION_STAGE")


def fetch_secret_version() -> str:
    client = boto3.client("secretsmanager")
    params = {"SecretId": _secret_id()}
    version_id = _version_id()
    version_stage = _version_stage()
    if version_id:
        params["VersionId"] = version_id
    if version_stage:
        params["VersionStage"] = version_stage
    response = client.get_secret_value(**params)
    return response.get("SecretString") or response["SecretBinary"].decode("utf-8")


if __name__ == "__main__":
    print(fetch_secret_version())
