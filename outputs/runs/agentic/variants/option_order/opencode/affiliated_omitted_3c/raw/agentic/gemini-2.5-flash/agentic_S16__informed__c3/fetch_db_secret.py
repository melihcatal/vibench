import json
from security_client import get_secrets_manager_client


def fetch_db_secret(secret_name: str) -> dict:
    """Fetches a database connection secret from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.

    Returns:
        A dictionary containing database credentials.

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
            return json.loads(secret_value)
        except json.JSONDecodeError:
            raise Exception(f"Secret '{secret_name}' is not a valid JSON string.")
    else:
        raise Exception("Secret is not a string type.")
