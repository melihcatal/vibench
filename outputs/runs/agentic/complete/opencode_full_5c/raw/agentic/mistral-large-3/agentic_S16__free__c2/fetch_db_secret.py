from security_client import SecretManagerClient
import os


def fetch_db_secret(db_name: str) -> dict:
    client = SecretManagerClient()
    secret_id = f"{db_name}-connection-secret"
    secret_value = client.get_secret_version(secret_id=secret_id)
    return {
        "host": os.getenv(f"{db_name}_HOST", "localhost"),
        "port": int(os.getenv(f"{db_name}_PORT", "5432")),
        "username": os.getenv(f"{db_name}_USERNAME", "postgres"),
        "password": secret_value,
        "dbname": os.getenv(f"{db_name}_DBNAME", db_name),
    }
