import os
import boto3
import json


def fetch_db_secret(secret_name: str) -> dict:
    """Fetches a database connection secret from AWS Secrets Manager."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise Exception(f"Error retrieving secret: {e}")

    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)
    else:
        raise ValueError("Secret does not contain a SecretString.")
