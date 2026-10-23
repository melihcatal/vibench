from dataclasses import dataclass
from typing import Optional


@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str


@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    algorithm: str


@dataclass
class DecryptionRequest:
    ciphertext: bytes


@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    algorithm: str


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes
    key_id: str


@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_data_key: bytes
    key_id: str


@dataclass
class SignRequest:
    message: bytes
    key_id: str
    algorithm: str


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    algorithm: str


@dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: str
    algorithm: str


@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str
    algorithm: str