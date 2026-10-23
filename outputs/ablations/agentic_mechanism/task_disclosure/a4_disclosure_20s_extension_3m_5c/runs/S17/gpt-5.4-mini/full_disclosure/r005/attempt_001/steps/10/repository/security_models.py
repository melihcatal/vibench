import base64
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64decode(data: str) -> bytes:
    if data.startswith("base64:"):
        data = data.split("base64:", 1)[1]
    return base64.b64decode(data)


def normalize_provider(provider: Optional[str]) -> str:
    value = (provider or "google_cloud_kms").strip().lower().replace("-", "_")
    if value in {"gcp_kms", "googlekms", "google_cloud_kms"}:
        return "google_cloud_kms"
    return value


def normalize_key_name(key_name: Optional[str], project_id: Optional[str] = None, location_id: Optional[str] = None, key_ring_id: Optional[str] = None, crypto_key_id: Optional[str] = None) -> str:
    if key_name:
        return key_name.strip()
    if all([project_id, location_id, key_ring_id, crypto_key_id]):
        return f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    raise ValueError("key_name or full GCP KMS key path must be provided")


@dataclass(frozen=True)
class EncryptionRequest:
    plaintext: str
    key_name: str
    associated_data: Optional[str] = None


@dataclass(frozen=True)
class DecryptionRequest:
    ciphertext: str
    key_name: str


@dataclass(frozen=True)
class EnvelopeEncryptionRequest:
    plaintext: str
    key_name: str
    associated_data: Optional[str] = None


@dataclass(frozen=True)
class SignatureRequest:
    key_name: str
    payload: str
    operation: str = "sign"
    signature: Optional[str] = None


@dataclass(frozen=True)
class EncryptionResponse:
    provider: str
    key_name: str
    ciphertext: str
    algorithm: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecryptionResponse:
    provider: str
    key_name: str
    plaintext: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EnvelopeEncryptionResponse:
    provider: str
    key_name: str
    encrypted_dek: str
    nonce: str
    ciphertext: str
    associated_data: Optional[str] = None
    algorithm: str = "AES-256-GCM"

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SignatureResponse:
    provider: str
    operation: str
    key_name: str
    signature: Optional[str] = None
    verified: Optional[bool] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_ciphertext(ciphertext: str) -> bytes:
    return _b64decode(ciphertext)


def encode_bytes(value: bytes) -> str:
    return _b64encode(value)
