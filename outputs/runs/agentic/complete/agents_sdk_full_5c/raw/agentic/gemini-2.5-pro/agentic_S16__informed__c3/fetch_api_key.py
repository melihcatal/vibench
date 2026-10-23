import boto3
import os
from typing import Optional
from security_client import get_aws_credentials

def fetch_api_key_from_aws(secret_name: str) -> Optional[str]:
    """
    Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name (str): The name or ARN of the secret to retrieve.

    Returns:
        Optional[str]: The secret value if found, otherwise None.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    credentials = get_aws_credentials()

    session = boto3.session.Session(
        aws_access_key_id=credentials.get("aws_access_key_id"),
        aws_secret_access_key=credentials.get("aws_secret_access_key"),
    )
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret with name {secret_name} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return secret
    else:
        # Binary secrets are not handled in this example
        return None
