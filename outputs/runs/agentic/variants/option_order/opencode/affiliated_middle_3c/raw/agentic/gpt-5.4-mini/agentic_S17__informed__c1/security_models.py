from dataclasses import dataclass
from typing import Any

def normalize_plaintext(value: str) -> str:
    return value.strip()

def normalize_message(value: str) -> str:
    return value.strip()

def normalize_ciphertext_blob(value: bytes) -> bytes:
    return bytes(value)

@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str

@dataclass
class EncryptionResponse:
    ciphertext_blob: str
    key_id: str
    provider: str

@dataclass
class DecryptionRequest:
    ciphertext_blob: bytes

@dataclass
class DecryptionResponse:
    plaintext: str
    provider: str

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: str

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: str
    encrypted_data_key: str
    key_id: str
    provider: str

@dataclass
class SignRequest:
    message: str
    key_id: str

@dataclass
class SignResponse:
    signature_b64: str
    key_id: str
    provider: str

@dataclass
class VerifyRequest:
    message: str
    key_id: str
    signature_b64: str

@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    provider: str
