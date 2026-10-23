import os
import json
import boto3
from botocore.exceptions import ClientError

def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key from AWS Secrets Manager."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise ValueError(f"Error fetching secret '{secret_name}': {e}") from e

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        try:
            # Assuming the API key is stored as a JSON string with a key, e.g., {"api_key": "YOUR_API_KEY"}
            secret_dict = json.loads(secret)
            return secret_dict.get("api_key")
        except json.JSONDecodeError:
            # If it's just the plain API key string
            return secret
    else:
        # For binary secrets, not typically used for API keys but handled for completeness
        raise NotImplementedError("Binary secret not handled for API key")
