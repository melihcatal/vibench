import os
from secret_clients import SecretsManagerClient


def fetch_db_secret() -> dict:
    """Fetches a database connection secret at runtime from Google Secret Manager.
    Returns:
        dict: The secret data containing database connection info.
    """
    client = SecretsManagerClient()
    response = client.get_secret_value(SecretId=os.getenv("DB_SECRET_ID"))
    return response["SecretString"]
