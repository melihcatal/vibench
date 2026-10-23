from security_client import SecretManagerClient


def fetch_api_key(secret_id: str) -> str:
    """Fetches an API key from Google Secret Manager."""
    client = SecretManagerClient()
    api_key = client.access_secret_version(secret_id)
    return api_key
