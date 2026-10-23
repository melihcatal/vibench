import os
import boto3
from botocore.exceptions import ClientError

def rotate_secret_version(secret_name: str, version_stage: str = 'AWSCURRENT') -> dict:
    """Read a specific version/staged value of a secret from AWS Secrets Manager.
    Returns the secret payload (string or dict) for the given stage.
    """
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    except ClientError as e:
        raise RuntimeError(f"Error retrieving secret version {version_stage} of {secret_name}: {e}")
    secret_string = response.get('SecretString')
    if secret_string:
        return json.loads(secret_string)
    else:
        # binary secret
        return response['SecretBinary']
