from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    encrypted_dek: Optional[bytes] = None # For envelope encryption

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    encrypted_dek: Optional[bytes] = None # For envelope encryption

@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str

@dataclass
class SignatureRequest:
    message: str
    key_version_id: str

@dataclass
class SignatureResponse:
    signature: bytes
    key_version_id: str

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class SafetyCheckResponse:
    text: str
    is_safe: bool
    scores: dict
