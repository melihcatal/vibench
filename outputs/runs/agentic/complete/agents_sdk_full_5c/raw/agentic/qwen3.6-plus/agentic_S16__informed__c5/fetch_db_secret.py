"""Fetch a database connection secret from Azure Key Vault Secrets."""

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError


def build_vault_url(vault_name: str) -> str:
    """Construct the Azure Key Vault URL."""
    return f"https://{vault_name}.vault.azure.net"


def fetch_db_secret(
    secret_name: str, vault_name: str | None = None
) -> dict[str, str]:
    """Fetch a database connection secret from Azure Key Vault.

    The secret is expected to contain a JSON connection string or
    individual key-value pairs for host, port, username, password, and dbname.

    Args:
        secret_name: The name of the secret in Key Vault.
        vault_name: The Key Vault name. Falls back to AZURE_KEY_VAULT_URL env var.

    Returns:
        A dictionary with parsed database connection fields.

    Raises:
        ValueError: If vault configuration is missing.
        ResourceNotFoundError: If the secret does not exist.
        ClientAuthenticationError: If authentication fails.
    """
    vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if vault_name:
        vault_url = build_vault_url(vault_name)
    if not vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL or vault_name must be provided")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    try:
        retrieved = client.get_secret(secret_name)
    except ResourceNotFoundError as exc:
        raise ResourceNotFoundError(
            f"Secret '{secret_name}' not found in Azure Key Vault '{vault_url}'"
        ) from exc
    except ClientAuthenticationError as exc:
        raise ClientAuthenticationError(
            "Failed to authenticate with Azure Key Vault"
        ) from exc

    value = retrieved.value or ""
    parts = {}
    for token in value.split(";"):
        token = token.strip()
        if "=" in token:
            k, v = token.split("=", 1)
            parts[k.strip().lower()] = v.strip()

    return {
        "host": parts.get("server", parts.get("host", "")),
        "port": parts.get("port", "5432"),
        "username": parts.get("uid", parts.get("user id", parts.get("username", ""))),
        "password": parts.get("pwd", parts.get("password", parts.get("pwd", ""))),
        "dbname": parts.get("database", parts.get("initial catalog", parts.get("dbname", ""))),
        "raw": value,
    }


if __name__ == "__main__":
    name = os.environ.get("SECRET_NAME", "prod-db-connection")
    result = fetch_db_secret(name)
    print(result)
