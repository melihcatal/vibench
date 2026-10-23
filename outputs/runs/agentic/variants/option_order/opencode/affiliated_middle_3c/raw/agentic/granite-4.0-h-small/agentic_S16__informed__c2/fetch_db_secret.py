import os
from security_client import SecretClientWrapper


def fetch_db_secret(secret_name: str) -> dict:
    """Fetches a database connection secret at runtime.
    Returns a dict with connection parameters (e.g., host, username, password).
    Uses the provider defined in SecretClientWrapper (e.g., AWS Secrets Manager).
    """
    client = SecretClientWrapper()
    response = client.get_secret(secret_name)
    return response.value  # expected to be a dict or JSON string
