from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    key_id: str
    algorithm: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    algorithm: Optional[str] = None

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    algorithm: str

@dataclass
class SignRequest:
    digest: bytes
    key_id: str
    algorithm: str

@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    algorithm: str

@dataclass
class VerifyRequest:
    digest: bytes
    signature: bytes
    key_id: str
    algorithm: str

@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str
    algorithm: str

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_key: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    key_id: str
    algorithm: str

@dataclass
class EnvelopeDecryptionRequest:
    ciphertext: bytes
    encrypted_key: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class EnvelopeDecryptionResponse:
    plaintext: bytes
    key_id: str
    algorithm: str
