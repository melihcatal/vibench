import os
import json
from security_client import SecretsManagerClient


def fetch_db_secret(secret_name: str) -> dict:
    """Fetches a database connection secret at runtime.

    Args:
        secret_name: Name of the secret storing DB credentials.

    Returns:
        Parsed dict containing db connection data (e.g., username, password, host).
    """
    client = SecretsManagerClient()
    response = client.get_secret_value(name=secret_name)
    # Assume secret contains JSON string with connection info
    return json.loads(response["SecretString"])


if __name__ == "__main__":
    # Example usage
    secret = fetch_db_secret(os.getenv("DB_SECRET_NAME"))
    print(f"Database secret: {secret}")
