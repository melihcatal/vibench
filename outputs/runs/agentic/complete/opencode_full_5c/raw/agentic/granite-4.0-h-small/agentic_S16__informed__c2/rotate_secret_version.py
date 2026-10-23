import os
import json
from dotenv import load_dotenv

load_dotenv()

# AWS Secrets Manager
import boto3

client = boto3.client("secretsmanager")


def rotate_secret_version(secret_name: str, version_stage: str = "AWSCURRENT"):
    response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    secret = json.loads(response["SecretString"])
    # Optionally update a staged version
    # Example: client.update_secret_version_stage(SecretId=secret_name, VersionId=secret['VersionId'], MoveToStage='AWSPREVIOUS')
    return secret
