import os


def provider_name():
    return "azure-keyvault-secrets"


def secret_vault_url():
    return os.getenv("AZURE_KEY_VAULT_URL", "")


def default_secret_name(name: str) -> str:
    return name.strip().replace(" ", "-")
