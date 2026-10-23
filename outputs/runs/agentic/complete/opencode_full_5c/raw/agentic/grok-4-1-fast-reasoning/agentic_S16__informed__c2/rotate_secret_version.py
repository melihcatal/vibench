import boto3
from security_client import get_aws_config


def rotate_secret_version(secret_name: str, version_stage: str = "AWSPENDING") -> str:
    config = get_aws_config()
    client = boto3.client("secretsmanager", **config)
    response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    return response["SecretString"]
