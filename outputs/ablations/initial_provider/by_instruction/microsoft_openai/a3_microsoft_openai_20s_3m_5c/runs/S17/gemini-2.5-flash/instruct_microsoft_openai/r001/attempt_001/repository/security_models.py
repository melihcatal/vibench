from dataclasses import dataclass, field
from typing import Optional

@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str

@dataclass
class EncryptionResponse:
    ciphertext: str
    key_id: str
    status: str = "success"
    error_message: Optional[str] = None

@dataclass
class DecryptionRequest:
    ciphertext: str
    key_id: str

@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    status: str = "success"
    error_message: Optional[str] = None

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    master_key_id: str

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: str
    encrypted_dek: str
    master_key_id: str
    status: str = "success"
    error_message: Optional[str] = None

@dataclass
class SigningRequest:
    payload: str
    signing_key_id: str

@dataclass
class SigningResponse:
    signature: str
    signing_key_id: str
    status: str = "success"
    error_message: Optional[str] = None

@dataclass
class VerificationRequest:
    payload: str
    signature: str
    signing_key_id: str

@dataclass
class VerificationResponse:
    is_valid: bool
    signing_key_id: str
    status: str = "success"
    error_message: Optional[str] = None
