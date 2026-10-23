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

@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: bytes

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str

@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: bytes

@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    ciphertext: bytes

@dataclass
class EnvelopeDecryptionRequest:
    key_id: str
    encrypted_data_key: bytes
    ciphertext: bytes

@dataclass
class SigningRequest:
    key_id: str
    message: bytes
    signing_algorithm: str

@dataclass
class SigningResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str

@dataclass
class VerificationRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str

@dataclass
class VerificationResponse:
    is_valid: bool
