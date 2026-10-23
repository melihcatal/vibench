import boto3

from security_client import load_security_config


def rotate_secret_version(version_stage: str = "AWSCURRENT") -> str:
    config = load_security_config("rotate/version")
    client = boto3.client("secretsmanager", region_name=config.aws_region)
    response = client.get_secret_value(
        SecretId=config.secret_id, VersionStage=version_stage
    )
    return response.get("SecretString", "")
