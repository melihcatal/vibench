import dataclasses
from typing import Optional

@dataclasses.dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    key_ring_id: Optional[str] = None

@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str

@dataclasses.dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: bytes
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    key_ring_id: Optional[str] = None

@dataclasses.dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str

@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext_data: bytes
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    key_ring_id: Optional[str] = None

@dataclasses.dataclass
class EnvelopeEncryptionResponse:
    encrypted_dek: bytes
    local_ciphertext: bytes
    key_id: str

@dataclasses.dataclass
class SignatureRequest:
    key_id: str
    key_version_id: str
    data: bytes
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    key_ring_id: Optional[str] = None

@dataclasses.dataclass
class SignatureResponse:
    signature: bytes
    key_id: str
    key_version_id: str

@dataclasses.dataclass
class VerificationRequest:
    key_id: str
    key_version_id: str
    data: bytes
    signature: bytes
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    key_ring_id: Optional[str] = None

@dataclasses.dataclass
class VerificationResponse:
    is_valid: bool
    key_id: str
    key_version_id: str
