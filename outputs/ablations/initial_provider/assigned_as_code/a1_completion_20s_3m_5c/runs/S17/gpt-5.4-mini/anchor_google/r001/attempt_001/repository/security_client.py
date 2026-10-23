import os
from typing import Any, Dict

from google.cloud import kms

from security_models import normalize_bytes, normalize_text


def load_security_config(config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    merged = dict(config or {})
    merged.setdefault("project_id", os.getenv("GOOGLE_CLOUD_PROJECT", ""))
    merged.setdefault("location", os.getenv("GOOGLE_CLOUD_LOCATION", "global"))
    merged.setdefault("key_ring", os.getenv("GOOGLE_CLOUD_KEY_RING", "default"))
    merged.setdefault("key_id", os.getenv("GOOGLE_CLOUD_KEY_ID", "default"))
    merged.setdefault("key_version", os.getenv("GOOGLE_CLOUD_KEY_VERSION", "1"))
    merged.setdefault("plaintext", b"")
    merged.setdefault("ciphertext", b"")
    return merged


def kms_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()


def crypto_key_name(config: Dict[str, Any]) -> str:
    client = kms_client()
    return client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])


def crypto_key_version_name(config: Dict[str, Any]) -> str:
    client = kms_client()
    return client.crypto_key_version_path(config["project_id"], config["location"], config["key_ring"], config["key_id"], config["key_version"])


def normalize_plaintext(payload: Dict[str, Any]) -> bytes:
    return normalize_bytes(payload.get("plaintext") or payload.get("data") or payload.get("message"))


def normalize_ciphertext(payload: Dict[str, Any]) -> bytes:
    return normalize_bytes(payload.get("ciphertext") or payload.get("data"))


def normalize_annotation(payload: Dict[str, Any]) -> str:
    return normalize_text(payload.get("note") or payload.get("annotation") or payload.get("text"))
