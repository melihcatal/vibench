from dataclasses import dataclass
from typing import Optional


@dataclass
class EncryptRequest:
    plaintext: bytes
    key_id: str


@dataclass
class EncryptResponse:
    ciphertext: bytes
    key_id: str


@dataclass
class DecryptRequest:
    ciphertext: bytes
    key_id: Optional[str] = None


@dataclass
class DecryptResponse:
    plaintext: bytes


@dataclass
class EnvelopeEncryptRequest:
    plaintext: bytes
    key_id: str


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: bytes
    ciphertext: bytes
    iv: bytes
    tag: bytes
    key_id: str


@dataclass
class SignRequest:
    message: bytes
    key_id: str


@dataclass
class SignResponse:
    signature: bytes


@dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: str
