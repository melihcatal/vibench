from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptionRequest:
    plaintext: bytes

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_version: str
    algorithm: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_version: str

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_dek: bytes
    iv: bytes
    algorithm: str

@dataclass
class SignRequest:
    digest: bytes
    data: bytes

@dataclass
class SignResponse:
    signature: bytes
    algorithm: str

@dataclass
class VerifyRequest:
    digest: bytes
    data: bytes
    signature: bytes

@dataclass
class VerifyResponse:
    is_valid: bool
    algorithm: str