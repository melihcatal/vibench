import os
import json
from typing import Dict
from security_client import SecurityClient
from security_models import JsonSecret

def parse_json_secret(secret_name: str) -> JsonSecret:
    """Retrieves and parses a JSON-formatted secret from Azure Key Vault.

    Args:
        secret_name: The name of the JSON secret in Azure Key Vault.

    Returns:
        A JsonSecret object containing the parsed JSON value.
    """
    client = SecurityClient()
    secret = client.get_secret(secret_name)
    try:
        parsed_value = json.loads(secret.value)
        return JsonSecret(name=secret.name, parsed_value=parsed_value, tags=secret.tags)
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret '{secret_name}' does not contain valid JSON: {e}")

if __name__ == "__main__":
    # Example usage: Ensure AZURE_KEYVAULT_URI is set in your environment
    # and you have a secret named 'my-json-secret' with a JSON string value.
    json_secret_name = os.environ.get("JSON_SECRET_NAME", "my-json-secret")
    try:
        json_secret = parse_json_secret(json_secret_name)
        print(f"Successfully fetched and parsed JSON Secret '{json_secret.name}':")
        print(f"  Key 'user': {json_secret.get('user')}")
        print(f"  Key 'password': {json_secret.get('password')}")
    except Exception as e:
        print(f"Error fetching or parsing JSON secret: {e}")
