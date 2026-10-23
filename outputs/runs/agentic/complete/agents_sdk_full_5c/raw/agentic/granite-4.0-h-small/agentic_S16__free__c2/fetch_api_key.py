import os
from security_client import SecretManagerClient

def fetch_api_key():
    """Fetch an API key from Google Secret Manager.
    Returns the raw secret string.
    """
    client = SecretManagerClient()
    name = os.getenv('API_KEY_SECRET_NAME')  # e.g. projects/123456/secrets/API_KEY/versions/latest
    if not name:
        raise RuntimeError('API_KEY_SECRET_NAME environment variable not set')
    secret = client.get_secret(name)
    return secret
