import json
from secret_clients import SecretsManagerClient


def parse_json_secret(secret_name: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from Azure Key Vault.
    Args:
        secret_name (str): Name of the secret to retrieve.
    Returns:
        dict: Parsed JSON data from the secret.
    """
    client = SecretsManagerClient()
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
