import os
import boto3
from botocore.exceptions import ClientError

def fetch_db_secret(secret_name: str) -> dict:
    """Fetch a database connection secret from AWS Secrets Manager.
    Returns a dict with keys: username, password, host, port, dbname.
    AWS credentials must be provided via environment variables or IAM role.
    """
    client = boto3.client('secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise RuntimeError(f"Failed to retrieve secret {secret_name}: {e}")
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)
