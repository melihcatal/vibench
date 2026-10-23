import os
from typing import Optional

# Placeholder names for concrete providers; these would be replaced with real SDK import paths.
# Example: from aws_kms import KMSClient for AWS KMS
# from azure_keyvault import KeyVaultClient for Azure Key Vault
# For demonstration we use environment variables to select the backend.

PROVIDER = os.getenv('ENCRYPTION_PROVIDER', 'aws')  # 'aws' or 'azure'


def get_kms_client() -> object:
    """Return a client object for the configured key management provider."""
    if PROVIDER == 'aws':
        # AWS KMS client via boto3 (installed SDK)
        import boto3
        return boto3.client('kms')
    elif PROVIDER == 'azure':
        # Azure Key Vault client via azure-keyvault-secrets
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient
        vault_uri = os.getenv('AZURE_KEYVAULT_URI')
        credential = DefaultAzureCredential()
        return SecretClient(vault_url=vault_uri, credential=credential)
    else:
        raise RuntimeError(f"Unsupported provider: {PROVIDER}")


def get_encryption_key_id() -> str:
    """Return the ID/ARN/URI of the default encryption key for the selected provider."""
    if PROVIDER == 'aws':
        return os.getenv('AWS_KMS_KEY_ID')  # e.g., arn:aws:kms:...
    elif PROVIDER == 'azure':
        return os.getenv('AZURE_KEYVAULT_KEY_NAME')  # name of the key in the vault
    raise RuntimeError("Key ID not configured for selected provider")


def get_data_key_id() -> str:
    """Return the same key used for data-encrypting key operations."""
    return get_encryption_key_id()  # reuse same key for simplicity


def get_smc_client() -> object:
    """Return a client for asymmetric signing/verification."""
    if PROVIDER == 'aws':
        import boto3
        return boto3.client('kms')
    elif PROVIDER == 'azure':
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.keys import CryptographyClient
        vault_uri = os.getenv('AZURE_KEYVAULT_URI')
        credential = DefaultAzureCredential()
        key_name = os.getenv('AZURE_KEYVAULT_SIGNING_KEY_NAME')
        key_vault_client = SecretClient(vault_url=vault_uri, credential=credential)
        return CryptographyClient(key_name, credential=credential, key_vault_url=vault_uri)
    raise RuntimeError("Unsupported provider for signing")
