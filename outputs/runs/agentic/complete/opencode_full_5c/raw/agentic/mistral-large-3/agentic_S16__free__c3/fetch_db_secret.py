import boto3
from botocore.exceptions import ClientError
import os


def fetch_db_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
    """
    Fetches a database connection secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret to fetch.
        region_name: AWS region where the secret is stored.

    Returns:
        The database connection secret as a dictionary.
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return eval(response["SecretString"])
    except ClientError as e:
        raise Exception(f"Failed to fetch secret: {e}")
