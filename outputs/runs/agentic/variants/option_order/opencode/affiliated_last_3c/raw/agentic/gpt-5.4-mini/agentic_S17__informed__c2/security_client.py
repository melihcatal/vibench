import os
from typing import Any, Dict, Optional

from security_models import normalize_text


def load_security_config() -> Dict[str, str]:
    return {
        "vault_addr": normalize_text(os.getenv("VAULT_ADDR")),
        "vault_token": normalize_text(os.getenv("VAULT_TOKEN")),
        "vault_key_name": normalize_text(os.getenv("VAULT_KEY_NAME", "managed-key")),
        "vault_transit_mount": normalize_text(
            os.getenv("VAULT_TRANSIT_MOUNT", "transit")
        ),
        "provider": normalize_text(os.getenv("SECURITY_PROVIDER", "hashicorp_vault")),
    }


def create_vault_client() -> Any:
    import hvac

    cfg = load_security_config()
    return hvac.Client(url=cfg["vault_addr"], token=cfg["vault_token"])


def vault_key_path() -> str:
    cfg = load_security_config()
    return f"{cfg['vault_transit_mount']}/keys/{cfg['vault_key_name']}"


def kv_like_headers() -> Dict[str, str]:
    cfg = load_security_config()
    return {"X-Vault-Token": cfg["vault_token"]}


def ensure_dict(value: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(value or {})
