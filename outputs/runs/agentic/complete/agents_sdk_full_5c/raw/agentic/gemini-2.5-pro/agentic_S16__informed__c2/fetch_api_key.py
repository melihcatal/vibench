import json
from security_client import get_secrets_manager_client
from security_models import ApiKey

def fetch_api_key(secret_name: str) -> ApiKey:
    """
    Fetches a secret from AWS Secrets Manager and parses it as an ApiKey.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        An ApiKey object.
    """
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    
    secret_data = json.loads(secret_string)
    return ApiKey(**secret_data)

