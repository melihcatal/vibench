import dataclasses
from typing import Optional


@dataclasses.dataclass
class EncryptRequest:
    key_id: str
    plaintext: bytes
    additional_authenticated_data: Optional[bytes] = None


@dataclasses.dataclass
class EncryptResponse:
    ciphertext: bytes


@dataclasses.dataclass
class DecryptRequest:
    key_id: str
    ciphertext: bytes
    additional_authenticated_data: Optional[bytes] = None


@dataclasses.dataclass
class DecryptResponse:
    plaintext: bytes


@dataclasses.dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: bytes
    additional_authenticated_data: Optional[bytes] = None


@dataclasses.dataclass
class EnvelopeEncryptResponse:
    encrypted_data_encryption_key: bytes
    ciphertext: bytes


@dataclasses.dataclass
class SignRequest:
    key_id: str
    digest: bytes  # SHA256, SHA384, or SHA512


@dataclasses.dataclass
class SignResponse:
    signature: bytes


@dataclasses.dataclass
class VerifyRequest:
    key_id: str
    digest: bytes
    signature: bytes


@dataclasses.dataclass
class VerifyResponse:
    is_valid: bool
