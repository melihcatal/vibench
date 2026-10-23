import boto3
import os

def get_secrets_manager_client():
    """
    Returns a boto3 Secrets Manager client.
    Assumes AWS credentials are configured in the environment or AWS config files.
    """
    return boto3.client(
        'secretsmanager',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
