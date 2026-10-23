from dataclasses import dataclass
import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient


@dataclass
class SecurityConfig:
    key_id: str
    vault_url: str | None = None
    algorithm: str = "A256GCM"


def load_security_config(config=None):
    data = dict(config or {})
    key_id = data.get("key_id") or os.environ["AZURE_KEYVAULT_KEY_ID"]
    return SecurityConfig(key_id=key_id, vault_url=data.get("vault_url"), algorithm=data.get("algorithm", "A256GCM"))


def build_crypto_client(config=None):
    security_config = load_security_config(config)
    credential = DefaultAzureCredential()
    client = CryptographyClient(security_config.key_id, credential=credential)
    return security_config, credential, client


def cleanup_client(credential=None, client=None):
    if client is not None:
        close = getattr(client, "close", None)
        if callable(close):
            close()
    if credential is not None:
        close = getattr(credential, "close", None)
        if callable(close):
            close()
