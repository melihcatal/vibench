# [SAME-SCENARIO] fetch_db_secret.py
import os
from security_client import SecretManagerClient

def fetch_db_secret():
    """Fetch database connection secret (username & password) from Azure Key Vault.

    Returns:
        dict: Dictionary with keys 'username' and 'password'.
    """
    client = SecretManagerClient(provider='azure')
    secret_name = os.getenv("DB_CREDENTIAL_SECRET_NAME")  # e.g. db-credentials
    if not secret_name:
        raise RuntimeError("DB_CREDENTIAL_SECRET_NAME environment variable not set")
    secret_blob = client.get_secret(secret_name)
    # Expected secret format: {"username": "user", "password": "pwd"}
    return secret_blob.decode('utf-8')
