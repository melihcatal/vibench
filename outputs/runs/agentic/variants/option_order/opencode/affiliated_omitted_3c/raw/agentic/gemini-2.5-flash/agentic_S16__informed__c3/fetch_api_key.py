import json
from security_client import get_secrets_manager_client


def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.

    Returns:
        The API key as a string.

    Raises:
        Exception: If the secret cannot be retrieved or parsed.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise Exception(f"Could not retrieve secret '{secret_name}': {e}")

    if "SecretString" in get_secret_value_response:
        secret_value = get_secret_value_response["SecretString"]
        try:
            # Assuming the API key might be stored as a simple string or within a JSON structure
            secret_json = json.loads(secret_value)
            if "api_key" in secret_json:
                return secret_json["api_key"]
            else:
                return secret_value  # If it's JSON but no 'api_key' field, return raw string
        except json.JSONDecodeError:
            return secret_value  # Not a JSON string, return as is
    else:
        # Binary secret (not expected for API key, but handled for completeness)
        raise Exception("Secret is not a string type.")
