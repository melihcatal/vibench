# [HELPER] security_client.py
# Local configuration and client helper utilities for Secret Management services

import os
from typing import Any, Dict

# Vault configuration (example using environment variables)
VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")


def init_vault_client() -> Any:
    """Initialize and return a HashiCorp Vault SDK client.

    Returns:
        A Vault client object ready for read/write operations.
    """
    from hashicorp.vault import Vault

    return Vault(address=VAULT_ADDR, token=VAULT_TOKEN)


# AWS Secrets Manager client (reused across functions)
secrets_client = boto3.client("secretsmanager")


def get_aws_secret(secret_id: str) -> dict:
    """Retrieve a secret from AWS Secrets Manager using the pre-configured client.

    Args:
        secret_id: Identifier of the secret.

    Returns:
        Parsed secret payload as a dictionary.
    """
    resp = secrets_client.get_secret_value(SecretId=secret_id)
    # Secrets Manager can return string or binary; we assume JSON string here
    if isinstance(resp["SecretString"], str):
        return json.loads(resp["SecretString"])
    return eval(
        resp["SecretBinary"]
    )  # Fallback for binary; replace with json.loads in real code
