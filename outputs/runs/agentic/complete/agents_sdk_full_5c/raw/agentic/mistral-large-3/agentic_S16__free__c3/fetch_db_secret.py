import os
import boto3
from botocore.exceptions import ClientError


def fetch_db_secret(secret_name: str, region_name: str = None) -> dict:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    
    Args:
        secret_name: The name of the secret (e.g., "prod/db/credentials").
        region_name: AWS region. Defaults to AWS_DEFAULT_REGION env var.
    
    Returns:
        The secret as a dictionary (e.g., {"username": "...", "password": "..."}).
    """
    if region_name is None:
        region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return eval(response["SecretString"])
    except ClientError as e:
        raise RuntimeError(f"Failed to fetch secret: {e}")