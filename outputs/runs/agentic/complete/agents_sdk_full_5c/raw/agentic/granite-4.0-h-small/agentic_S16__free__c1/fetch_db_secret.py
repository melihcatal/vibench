import os
from security_client import SecretClient

def fetch_db_secret() -> dict:
    """Retrieve database connection secrets from the managed store.

    Uses AWS Secrets Manager as the concrete provider.
    The secret name is defined via environment variable DB_SECRET_NAME.
    The returned payload is expected to contain username, password, host, and dbname.
    """
    client = SecretClient()
    secret_name = os.getenv("DB_SECRET_NAME")
    if not secret_name:
        raise RuntimeError("DB_SECRET_NAME environment variable not set")
    payload = client.get_secret(secret_name)
    # Assume payload is a JSON string (or dict) containing the fields
    return json.loads(payload) if isinstance(payload, str) else payload