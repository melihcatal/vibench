# [SAME-SCENARIO] rotate_secret_version.py
# Reads a specific secret version or staged value from AWS Secrets Manager

import os
import boto3


def rotate_secret_version(secret_name: str, version_stage: str = "AWSCURRENT") -> dict:
    """Retrieve a specific version or staged value of a secret.
    Args:
        secret_name: The secret identifier.
        version_stage: Version identifier; defaults to 'AWSCURRENT'.
    Returns:
        The secret payload (dict) for the requested version.
    Raises:
        Exception if retrieval fails.
    """
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    if "SecretString" in response:
        return json.loads(response["SecretString"])
    else:
        secret_bytes = base64.b64decode(response["SecretBinary"])
        return json.loads(secret_bytes.decode("utf-8"))
