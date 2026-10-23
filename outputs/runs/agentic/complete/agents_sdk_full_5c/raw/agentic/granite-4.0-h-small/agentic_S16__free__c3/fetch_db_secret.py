# fetch_db_secret.py
import os
from security_client import get_secret_manager_client

def fetch_db_secret(secret_name: str) -> dict:
    """Retrieve a database connection secret.

    Uses HashiCorp Vault as the concrete provider.
    Returns the secret payload as a dict.
    """
    client = get_secret_manager_client()
    response = client.read_secret(path=secret_name)
    return response['data'].get('data', {})
