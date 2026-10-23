import os
from secret_clients import SecretsManagerClient


def fetch_api_key() -> str:
    """Fetches an API key from AWS Secrets Manager.
    Returns:
        str: The retrieved API key.
    """
    client = SecretsManagerClient()
    response = client.get_secret_value(SecretId=os.getenv("API_KEY_SECRET_ID"))
    return response["SecretString"]
