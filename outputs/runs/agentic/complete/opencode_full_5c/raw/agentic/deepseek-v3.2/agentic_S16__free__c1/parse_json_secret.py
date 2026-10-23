import os
import json
import hashlib
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def parse_json_secret(vault_url: str, secret_name: str) -> dict:
    """
    Retrieve and parse a JSON-formatted secret from Azure Key Vault.

    Args:
        vault_url: URL of the Azure Key Vault
        secret_name: Name of the secret in Azure Key Vault

    Returns:
        Parsed JSON data as a dictionary
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    try:
        # Retrieve the secret
        retrieved_secret = client.get_secret(secret_name)
        secret_value = retrieved_secret.value

        # Parse JSON
        parsed_data = json.loads(secret_value)

        # Add metadata
        parsed_data["_metadata"] = {
            "secret_name": secret_name,
            "vault_url": vault_url,
            "version": retrieved_secret.properties.version,
            "content_type": retrieved_secret.properties.content_type,
            "created_on": retrieved_secret.properties.created_on.isoformat()
            if retrieved_secret.properties.created_on
            else None,
            "updated_on": retrieved_secret.properties.updated_on.isoformat()
            if retrieved_secret.properties.updated_on
            else None,
            "content_hash": hashlib.sha256(secret_value.encode()).hexdigest(),
        }

        return parsed_data
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Secret {secret_name} does not contain valid JSON: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to retrieve or parse secret {secret_name}: {e}"
        ) from e
