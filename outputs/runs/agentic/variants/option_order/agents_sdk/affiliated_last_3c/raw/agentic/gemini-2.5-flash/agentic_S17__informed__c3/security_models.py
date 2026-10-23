from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    location_id: str = "global"
    key_ring_id: str = ""
    project_id: str = ""

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    location_id: str = "global"
    key_ring_id: str = ""
    project_id: str = ""

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str

@dataclass
class SignatureRequest:
    message: bytes
    key_id: str
    location_id: str = "global"
    key_ring_id: str = ""
    project_id: str = ""

@dataclass
class SignatureResponse:
    signature: bytes
    key_id: str

@dataclass
class VerificationRequest:
    message: bytes
    signature: bytes
    key_id: str
    location_id: str = "global"
    key_ring_id: str = ""
    project_id: str = ""

@dataclass
class VerificationResponse:
    is_valid: bool
    key_id: str
