import json
import boto3

# AWS Secrets Manager


def rotate_secret_version(secret_id: str, version_stage: str = "AWSCURRENT") -> str:
    """Read a specific secret version or staged value from AWS Secrets Manager.

    Returns the raw secret string for the requested version/stage.
    """
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id, VersionStage=version_stage)
    return response["SecretString"]
