from dataclasses import dataclass
from typing import Optional


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes


@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    algorithm: str


@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: Optional[str] = None


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    algorithm: str


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: str


@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_dek: bytes
    iv: bytes
    key_id: str


@dataclass
class SignRequest:
    key_id: str
    message: bytes
    algorithm: str


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    algorithm: str


@dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    algorithm: str


@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str
    algorithm: str