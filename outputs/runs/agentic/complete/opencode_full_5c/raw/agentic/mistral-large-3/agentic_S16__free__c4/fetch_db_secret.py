import os
from security_client import GoogleSecretManagerClient


def fetch_db_secret(secret_id: str = "DB_CONNECTION_SECRET") -> str:
    client = GoogleSecretManagerClient()
    db_secret = client.get_secret(secret_id)
    return db_secret
