import boto3
from security_models import SecretResponse

def rotation_summary(secret_id='ROTATING-API-KEY') -> str:
    client = boto3.client('secretsmanager')
    metadata = client.describe_secret(SecretId=secret_id)
    last_rotated = metadata.get('LastRotatedDate')
    next_rotation = metadata.get('NextRotationDate')
    staged_version = client.get_secret_value(SecretId=secret_id, VersionStage='AWSPENDING')
    return f"Last rotated: {last_rotated}, next scheduled: {next_rotation}, pending version: {staged_version['VersionId']}"
