import os
from typing import Any, Dict

from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient


def load_security_config(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    config = {
        "key_id": os.environ.get("AZURE_KEY_VAULT_KEY_ID"),
        "vault_url": os.environ.get("AZURE_KEY_VAULT_URL"),
        "translation_endpoint": os.environ.get("AZURE_TRANSLATOR_ENDPOINT"),
        "translation_key": os.environ.get("AZURE_TRANSLATOR_KEY"),
        "translation_region": os.environ.get("AZURE_TRANSLATOR_REGION"),
    }
    if overrides:
        config.update({k: v for k, v in overrides.items() if v is not None})
    return config


def create_credential() -> DefaultAzureCredential:
    return DefaultAzureCredential()


def create_crypto_client(key_id: str, credential=None) -> CryptographyClient:
    credential = credential or create_credential()
    return CryptographyClient(key_id, credential=credential)
