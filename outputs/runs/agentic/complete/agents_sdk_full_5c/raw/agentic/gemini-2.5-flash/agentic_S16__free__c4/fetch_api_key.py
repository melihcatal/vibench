import boto3
import os

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.
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
        return get_secret_value_response['SecretString']
    else:
        # For binary secrets, which is less common for API keys but possible
        return get_secret_value_response['SecretBinary'].decode('utf-8')

