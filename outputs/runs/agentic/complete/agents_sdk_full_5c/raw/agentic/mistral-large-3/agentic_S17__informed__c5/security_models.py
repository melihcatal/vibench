from dataclasses import dataclass
from typing import Optional, Union


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
    key_id: str


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
    encrypted_dek: bytes
    nonce: bytes
    key_id: str
    algorithm: str


@dataclass
class SignRequest:
    payload: bytes
    key_id: str


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    algorithm: str


@dataclass
class VerifyRequest:
    payload: bytes
    signature: bytes
    key_id: str


@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str
    algorithm: str