# security_models.py
# Local request/response model helpers for Key Management and Encryption services

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
#  Key Management Models
# ---------------------------------------------------------------------------


@dataclass
# HashiCorp Vault - KV v2 secret

# Example response from Vault read_secret_version
# {"data": {"data": {"value": "<b64-key>", "...": "..."}}
# We expose just the raw decoded key.
class VaultKvSecret:
    raw_b64: str  # base64‑encoded key material (e.g., Fernet key)
    version: Optional[int] = None  # Vault version metadata (optional)

    def unwrap(self) -> bytes:
        import base64

        return base64.b64decode(self.raw_b64)


@dataclass
# Azure Key Vault Key - simplified representation of a RSA / EC key

class AzureKey:
    key_id: str  # Full Azure key identifier (e.g., "https://.../keys/KeyName")
    kty: str  # Key type (RSA, EC, Oct)
    value: Optional[str] = (
        None  # PEM or JWK representation, if stored in Vault for cross‑cloud sync
    )


@dataclass
class AlibabaKmsKey:
    key_id: str  # Alibaba KMS key ID or ARN
    key_spec: str = "AES_256"  # Spec returned by DescribeKey
    key_usage: str = "ENCRYPT/DECRYPT"


@dataclass
class GoogleKmsCryptoKey:
    name: str  # Full resource name, e.g., "projects/.../locations/.../keyRings/.../cryptoKeys/..."
    primary: Optional[Dict[str, Any]] = None  # Primary key version metadata
    rotations: Optional[Dict[str, Any]] = None  # creation/next rotate times


@dataclass
class IBMKeyProtectKey:
    key_id: str  # Key CRN (e.g., "crn:v1:...:key:..." )
    algorithm: str = "AES_BCM"  # Algorithm used for protection
    mode: str = "cbc"  # Encryption mode (if applicable)


# ---------------------------------------------------------------------------
#  Encryption / Signing Model Helpers
# ---------------------------------------------------------------------------


@dataclass
class EncryptionEnvelope:
    ciphertext: bytes  # Raw encrypted bytes (payload)
    iv: bytes  # Initialization vector used (if applicable)
    wrapped_dek: Optional[bytes] = (
        None  # DEK encrypted by a KMS (e.g., Vault transit) – optional for envelope mode
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext": self.ciphertext.hex(),
            "iv": self.iv.hex() if self.iv else None,
            "wrapped_dek": self.wrapped_dek.hex() if self.wrapped_dek else None,
        }


@dataclass
# Simple generic request wrapper for downstream services (e.g., API calls)
class ServiceRequest:
    endpoint: str
    payload: Any
    headers: Optional[Dict[str, str]] = None

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
#  Normalization utilities
# ---------------------------------------------------------------------------


def normalize_key_id(identifier: str, provider: str) -> str:
    """Return a canonical key identifier string based on provider spec."""
    if provider.lower() == "vault":
        return f"vault:{identifier}".strip()
    elif provider.lower() == "azure":
        return f"azure:{identifier}".strip()
    elif provider.lower() == "alibaba":
        return f"alibaba:{identifier}".strip()
    elif provider.lower() == "google":
        return f"google:{identifier}".strip()
    elif provider.lower() == "ibm":
        return f"ibm:{identifier}".strip()
    else:
        raise ValueError(f"Unknown provider {provider}")


# ---------------------------------------------------------------------------
# End of module
