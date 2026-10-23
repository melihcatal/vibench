# HELPER: security_models.py
"""Local request/response normalization models for Key Management & Encryption.

These simple dataclasses are used by the SCORED implementation files to
ensure a consistent JSON-serializable contract when interacting with external
providers. They also provide simple validation methods (e.g., asserting that
a provider name appears in a whitelisted set).
"""

from dataclasses import dataclass
from typing import Optional
import base64
import json

#: Whitelisted provider identifiers used by the helper functions
PROVIDER_WHITELIST = {"google-kms", "google-kms-envelope"}


def validate_provider(provider: str) -> None:
    if provider not in PROVIDER_WHITELIST:
        raise ValueError(
            f"Unsupported provider: {provider}. Must be one of {list(PROVIDER_WHITELIST)}"
        )


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
@dataclass
class EncryptRequest:
    """Payload to be encrypted."""

    plaintext: bytes
    provider: str = "google-kms"

    def validate(self) -> None:
        validate_provider(self.provider)


@dataclass
class DecryptRequest:
    """Ciphertext to be decrypted."""

    ciphertext_b64: str
    provider: str = "google-kms"

    def validate(self) -> None:
        validate_provider(self.provider)


@dataclass
class EnvelopeEncryptRequest:
    """Envelope encryption request."""

    plaintext: str
    envelope_key_id: Optional[str] = None
    provider: str = "google-kms-envelope"

    def validate(self) -> None:
        validate_provider(self.provider)


@dataclass
class SignOrVerifyRequest:
    """Signing or verification payload."""

    payload: dict
    action: str  # "sign" or "verify"
    key_id: str

    def validate(self) -> None:
        if self.action not in {"sign", "verify"}:
            raise ValueError(f"Unsupported action: {self.action}")


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------
@dataclass
class EncryptResponse:
    """Result of a symmetric encryption."""

    key_id: str
    ciphertext_b64: str
    provider: str

    def to_dict(self) -> dict:
        return {
            "key_id": self.key_id,
            "ciphertext_b64": self.ciphertext_b64,
            "provider": self.provider,
        }


@dataclass
class DecryptResponse:
    """Result of a symmetric decryption."""

    key_id: str
    plaintext: str
    provider: str

    def to_dict(self) -> dict:
        return {
            "key_id": self.key_id,
            "plaintext": self.plaintext,
            "provider": self.provider,
        }


@dataclass
class EnvelopeEncryptResponse:
    """Envelope encryption result: encrypted DEK + encrypted payload."""

    encrypted_dek: str  # base64 ciphertext of DEK
    iv: str  # base64 IV for AES CBC
    payload: str  # base64 ciphertext produced by KMS
    provider: str

    def to_dict(self) -> dict:
        return {
            "encrypted_dek": self.encrypted_dek,
            "iv": self.iv,
            "payload": self.payload,
            "provider": self.provider,
        }


@dataclass
class SignOrVerifyResponse:
    """Result of a signing or verification operation."""

    success: bool
    result: Optional[str] = None
    provider: str

    def to_dict(self) -> dict:
        d = {"success": self.success, "provider": self.provider}
        if self.result is not None:
            d["result"] = self.result
        return d


# ---------------------------------------------------------------------------
# Helper to convert raw dictionaries (e.g., from JSON) into the models
# ---------------------------------------------------------------------------


def from_dict(d: dict, cls) -> object:
    return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields})


# ---------------------------------------------------------------------------
# End of models module
# ---------------------------------------------------------------------------
# Local demo (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("security_models loaded - safe for import.")
