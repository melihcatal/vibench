import os
import json
from security_client import SecretClient

def fetch_api_key() -> str:
    """Retrieve the API key secret from the managed secrets store.
    
    Uses Google Secret Manager as the concrete provider.
    The secret ID is defined via environment variable SECRET_ID.
    """
    client = SecretClient()
    secret_id = os.getenv("SECRET_ID")
    if not secret_id:
        raise RuntimeError("SECRET_ID environment variable not set")
    api_key = client.get_secret(secret_id)
    return api_key