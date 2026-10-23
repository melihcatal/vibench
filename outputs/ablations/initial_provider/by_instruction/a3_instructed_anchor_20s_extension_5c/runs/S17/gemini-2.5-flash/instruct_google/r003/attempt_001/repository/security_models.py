from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: Optional[str] = None

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str

@dataclass
class DecryptionResponse:
    plaintext: bytes

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes
    key_id: Optional[str] = None

@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    local_ciphertext: bytes
    key_id: str

@dataclass
class SignatureRequest:
    message_digest: bytes
    key_id: str
    version_id: str

@dataclass
class SignatureResponse:
    signature: bytes
    key_id: str
    version_id: str

@dataclass
class VerificationRequest:
    message_digest: bytes
    signature: bytes
    key_id: str
    version_id: str

@dataclass
class VerificationResponse:
    is_valid: bool
