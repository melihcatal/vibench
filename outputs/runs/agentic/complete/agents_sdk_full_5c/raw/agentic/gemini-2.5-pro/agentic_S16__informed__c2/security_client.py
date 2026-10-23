import os
import boto3

def get_secrets_manager_client():
    """
    Initializes and returns a Boto3 client for AWS Secrets Manager.
    
    Expects AWS credentials and region to be configured in the environment
    (e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION).
    """
    return boto3.client(
        service_name='secretsmanager',
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
