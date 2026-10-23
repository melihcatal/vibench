import os
from security_client import get_secrets_manager_client

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        The API key as a string.

    Raises:
        ClientError: If the secret cannot be retrieved.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving secret '{secret_name}': {e}")

    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on your needs, you might need to decode the binary data.
        return get_secret_value_response['SecretBinary'].decode('utf-8')
