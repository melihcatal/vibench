from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes
    context: Optional[Dict[str, str]] = None

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    success: bool = True
    error: Optional[str] = None

@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: bytes
    context: Optional[Dict[str, str]] = None

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    success: bool = True
    error: Optional[str] = None

@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: bytes
    context: Optional[Dict[str, str]] = None

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_data_key: bytes
    success: bool = True
    error: Optional[str] = None

@dataclass
class SigningRequest:
    key_id: str
    key_version: str
    data_to_sign: bytes
    algorithm: str # e.g., 'RS256'

@dataclass
class SigningResponse:
    signature: bytes
    key_id: str
    algorithm: str
    success: bool = True
    error: Optional[str] = None

@dataclass
class VerificationRequest:
    key_id: str
    key_version: str
    data_to_verify: bytes
    signature: bytes
    algorithm: str

@dataclass
class VerificationResponse:
    is_valid: bool
    key_id: str
    algorithm: str
    success: bool = True
    error: Optional[str] = None
