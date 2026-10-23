import base64
import os
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet


PROVIDER_NAME = "hashicorp_vault"
VAULT_ADDR_ENV = "VAULT_ADDR"
VAULT_TOKEN_ENV = "VAULT_TOKEN"


def load_security_settings() -> Dict[str, str]:
    addr = os.getenv(VAULT_ADDR_ENV, "http://127.0.0.1:8200")
    token = os.getenv(VAULT_TOKEN_ENV, "")
    return {"provider": PROVIDER_NAME, "vault_addr": addr, "vault_token": token}


def get_vault_client() -> Any:
    from hvac import Client

    settings = load_security_settings()
    return Client(url=settings["vault_addr"], token=settings["vault_token"])


def get_transit() -> Any:
    client = get_vault_client()
    return client.secrets.transit


def ensure_bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    return str(value).encode("utf-8")


def to_base64_text(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def from_base64_text(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def derive_data_key() -> bytes:
    return Fernet.generate_key()


def local_fallback_fernet(key_material: Optional[bytes] = None) -> Fernet:
    return Fernet(key_material or Fernet.generate_key())
