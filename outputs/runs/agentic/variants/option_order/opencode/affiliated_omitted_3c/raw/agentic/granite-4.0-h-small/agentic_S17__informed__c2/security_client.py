# [HELPER] security_client.py - Provide local configuration and client helper utilities for Key Management and Encryption

import os
from typing import Any, Dict, Optional

# Supported providers (add/remove as needed)
PROVIDERS = {
    "gcp_kms": {
        "service": "Google Cloud KMS",
        "module": "google.cloud.kms",
        "client_class": "KeyManagementServiceClient",
        "creds_env": "GOOGLE_APPLICATION_CREDENTIALS",
    },
    "aws_kms": {
        "service": "AWS Key Management Service",
        "module": "boto3",
        "client_func": "client('kms')",
        "creds_env": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
    },
    "hashicorp_vault": {
        "service": "HashiCorp Vault",
        "module": "hvac",
        "client_class": "Client",
        "creds_env": ["VAULT_ADDR", "VAULT_TOKEN"],
    },
    "azure_keyvault": {
        "service": "Azure Key Vault Keys",
        "module": "azure-keyvault-keys",
        "client_class": "CertificateClient",
        "creds_env": [
            "AZURE_KEY_VAULT_URL",
            "AZURE_CLIENT_ID",
            "AZURE_TENANT_ID",
            "AZURE_CLIENT_SECRET",
        ],
    },
}


def get_client(provider_name: str, **extra_kwargs: Any) -> Any:
    """Returns an instantiated client for the given provider using environment variables for credentials.

    Args:
        provider_name: Key in PROVIDERS (e.g., 'gcp_kms').
        extra_kwargs: Additional arguments passed to the client constructor/factory.

    Raises:
        ValueError: If the provider is unknown or credentials are missing.
    """
    info = PROVIDERS.get(provider_name)
    if not info:
        raise ValueError(f"Unknown provider: {provider_name}")

    # Check required environment variables
    missing = []
    if info.get("creds_env"):
        if isinstance(info["creds_env"], list):
            for var in info["creds_env"]:
                if not os.getenv(var):
                    missing.append(var)
        elif isinstance(info["creds_env"], str):
            if not os.getenv(info["creds_env"]):
                missing.append(info["creds_env"])
    if missing:
        raise ValueError(
            f"Missing environment variables for {provider_name}: {', '.join(missing)}"
        )

    # Import the module lazily
    try:
        module = __import__(info["module"], fromlist=["dummy"])
    except ImportError as e:
        raise ImportError(f"Cannot import provider module {info['module']}: {e}")

    # Instantiate client
    if info.get("client_class"):
        client_class = getattr(module, info["client_class"])
        return client_class(**extra_kwargs)
    elif info.get("client_func"):
        return eval(
            info["client_func"], globals()
        )  # simple evaluation for boto3 client example
    else:
        raise NotImplementedError("Provider configuration incomplete")


if __name__ == "__main__":
    # Demo usage – list supported providers
    print(json.dumps(PROVIDERS, indent=2))
