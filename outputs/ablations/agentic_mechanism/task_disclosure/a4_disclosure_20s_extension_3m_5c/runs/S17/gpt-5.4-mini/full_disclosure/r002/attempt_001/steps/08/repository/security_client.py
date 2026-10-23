import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import kms


DEFAULT_KMS_KEY_NAME_ENV = "GOOGLE_CLOUD_KMS_KEY_NAME"


@dataclass(frozen=True)
class SecurityClientConfig:
    key_name: Optional[str] = None
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    key_ring_id: Optional[str] = None
    crypto_key_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "SecurityClientConfig":
        key_name = os.environ.get(DEFAULT_KMS_KEY_NAME_ENV)
        return cls(
            key_name=key_name,
            project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location_id=os.environ.get("GOOGLE_CLOUD_KMS_LOCATION"),
            key_ring_id=os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING"),
            crypto_key_id=os.environ.get("GOOGLE_CLOUD_KMS_CRYPTO_KEY"),
        )

    def resolved_key_name(self) -> str:
        if self.key_name:
            return self.key_name
        parts = [self.project_id, self.location_id, self.key_ring_id, self.crypto_key_id]
        if any(part is None for part in parts):
            raise KeyError(DEFAULT_KMS_KEY_NAME_ENV)
        return (
            f"projects/{self.project_id}/locations/{self.location_id}"
            f"/keyRings/{self.key_ring_id}/cryptoKeys/{self.crypto_key_id}"
        )


def load_config() -> SecurityClientConfig:
    return SecurityClientConfig.from_env()


def load_key_name(key_name: Optional[str] = None) -> str:
    if key_name:
        return key_name
    return load_config().resolved_key_name()


def kms_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()


def normalize_bytes_payload(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        try:
            data = json.loads(value)
            if isinstance(data, dict):
                value = data.get("plaintext_b64") or data.get("plaintext") or data.get("payload") or data
        except json.JSONDecodeError:
            pass
        if isinstance(value, str):
            try:
                return base64.b64decode(value)
            except Exception:
                return value.encode("utf-8")
    if isinstance(value, dict):
        nested = value.get("plaintext_b64") or value.get("plaintext") or value.get("payload")
        if nested is not None:
            return normalize_bytes_payload(nested)
    raise TypeError("Unsupported payload type")


def normalize_b64_payload(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def client_metadata() -> Dict[str, Any]:
    config = load_config()
    return {
        "provider": "google_cloud_kms",
        "key_name": config.key_name,
        "resolved_key_name": config.key_name or config.resolved_key_name(),
        "project_id": config.project_id,
        "location_id": config.location_id,
        "key_ring_id": config.key_ring_id,
        "crypto_key_id": config.crypto_key_id,
    }
