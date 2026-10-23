import os
from security_client import SecretClientWrapper


def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key from the configured secret manager.
    Uses the provider identified in SecretClientWrapper (e.g., Azure Key Vault).
    Returns the plain text API key as a string.
    """
    client = SecretClientWrapper()
    response = client.get_secret(secret_name)
    # Assume response.value contains the secret payload
    return response.value
