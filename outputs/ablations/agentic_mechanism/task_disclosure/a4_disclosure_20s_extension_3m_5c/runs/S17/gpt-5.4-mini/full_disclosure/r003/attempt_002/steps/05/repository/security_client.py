import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import kms_v1


@dataclass(frozen=True)
class SecurityConfig:
    project_id: str
    location_id: str = "global"
    key_ring_id: Optional[str] = None
    crypto_key_id: Optional[str] = None
    key_version_id: Optional[str] = None
    plaintext_encoding: str = "utf-8"

    @property
    def resource_prefix(self) -> str:
        if self.key_ring_id and self.crypto_key_id:
            return f"projects/{self.project_id}/locations/{self.location_id}/keyRings/{self.key_ring_id}/cryptoKeys/{self.crypto_key_id}"
        return ""


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def load_security_config(prefix: str = "SECURITY_") -> SecurityConfig:
    project_id = _env(f"{prefix}PROJECT_ID")
    if not project_id:
        raise ValueError("Missing required environment variable: SECURITY_PROJECT_ID")
    return SecurityConfig(
        project_id=project_id,
        location_id=_env(f"{prefix}LOCATION_ID", "global") or "global",
        key_ring_id=_env(f"{prefix}KEY_RING_ID"),
        crypto_key_id=_env(f"{prefix}CRYPTO_KEY_ID"),
        key_version_id=_env(f"{prefix}KEY_VERSION_ID"),
        plaintext_encoding=_env(f"{prefix}PLAINTEXT_ENCODING", "utf-8") or "utf-8",
    )


@lru_cache(maxsize=1)
def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def crypto_key_path(config: SecurityConfig) -> str:
    if not (config.key_ring_id and config.crypto_key_id):
        raise ValueError("key_ring_id and crypto_key_id are required")
    return f"projects/{config.project_id}/locations/{config.location_id}/keyRings/{config.key_ring_id}/cryptoKeys/{config.crypto_key_id}"


def crypto_key_version_path(config: SecurityConfig) -> str:
    if not config.key_version_id:
        raise ValueError("key_version_id is required")
    return f"{crypto_key_path(config)}/cryptoKeyVersions/{config.key_version_id}"


def plaintext_to_bytes(data: str, config: Optional[SecurityConfig] = None) -> bytes:
    encoding = config.plaintext_encoding if config else "utf-8"
    return data.encode(encoding)


def bytes_to_plaintext(data: bytes, config: Optional[SecurityConfig] = None) -> str:
    encoding = config.plaintext_encoding if config else "utf-8"
    return data.decode(encoding)
