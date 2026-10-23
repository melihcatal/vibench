import os
from typing import Optional

import boto3


def rotate_secret_version(secret_id: str, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> str:
    client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    kwargs = {"SecretId": secret_id}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage
    response = client.get_secret_value(**kwargs)
    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        return ""
    return secret_binary.decode("utf-8")
