import boto3
import os

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.
    """
    client = boto3.client(
        'secretsmanager',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            # Handle binary secrets if needed, but for API keys, SecretString is expected
            raise ValueError("SecretString not found in the response.")
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        raise

