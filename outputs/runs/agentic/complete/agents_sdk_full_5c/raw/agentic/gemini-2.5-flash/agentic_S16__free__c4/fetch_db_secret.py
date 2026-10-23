import boto3
import os
import json

def fetch_db_secret(secret_name: str) -> dict:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    The secret is expected to be a JSON string.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise RuntimeError(f"Could not retrieve secret {secret_name}: {e}")

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        raise ValueError(f"Secret {secret_name} is not a string secret.")

