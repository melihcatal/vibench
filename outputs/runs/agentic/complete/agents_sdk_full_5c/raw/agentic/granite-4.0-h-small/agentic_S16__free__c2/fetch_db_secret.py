import os
from security_client import SecretManagerClient

def fetch_db_secret():
    """Retrieve a database connection secret from AWS Secrets Manager.
    Returns a dict with keys: username, password, host, dbname.
    """
    client = SecretManagerClient(provider='aws')
    secret_name = os.getenv('DB_SECRET_NAME')
    if not secret_name:
        raise RuntimeError('DB_SECRET_NAME environment variable not set')
    secret = client.get_secret(secret_name)
    # Assume secret is a JSON string containing the credentials
n   import json
    return json.loads(secret)
