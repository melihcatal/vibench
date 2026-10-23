import os

from security_client import fetch_secret_value


def fetch_db_secret() -> str:
    secret_name = os.getenv("DB_SECRET_NAME", "db-connection")
    return fetch_secret_value(secret_name)
