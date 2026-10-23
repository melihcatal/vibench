import boto3
import os

def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key from AWS Secrets Manager."""
    client = boto3.client(
        'secretsmanager',
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            # Handle binary secrets if needed, but API keys are typically strings
            return get_secret_value_response['SecretBinary'].decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Could not retrieve secret {secret_name}: {e}")

