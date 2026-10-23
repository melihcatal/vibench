import os

import boto3


def rotation_summary() -> str:
    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION"))
    secret_id = os.environ.get("SECRET_NAME", "rotating-secret")
    response = client.describe_secret(SecretId=secret_id)
    versions = response.get("VersionIdsToStages", {})
    return f"{secret_id}:{len(versions)} versions"
