from dataclasses import dataclass
from typing import Optional


@dataclass
class EncryptionPayload:
    key_id: str
    plaintext: bytes


@dataclass
class DecryptionPayload:
    key_id: str
    ciphertext: bytes


@dataclass
class SignPayload:
    key_id: str
    message: bytes
    signing_algorithm: str


@dataclass
class VerifyPayload:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str


@dataclass
class EnvelopeEncryptionPayload:
    key_id: str
    plaintext: bytes


@dataclass
class EnvelopeDecryptionResult:
    plaintext: bytes


@dataclass
class EnvelopeEncryptionResult:
    ciphertext: bytes
    encrypted_data_key: bytes
    iv: bytes
    tag: bytes


@dataclass
class EnvelopeDecryptionPayload:
    encrypted_data_key: bytes
    ciphertext: bytes
    iv: bytes
    tag: bytes
