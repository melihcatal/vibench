from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: bytes

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_version_name: Optional[str] = None

@dataclass
class DecryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: bytes

@dataclass
class DecryptionResponse:
    plaintext: bytes

@dataclass
class SigningRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    key_version_id: str
    message: bytes

@dataclass
class SigningResponse:
    signature: bytes

@dataclass
class VerificationRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    key_version_id: str
    message: bytes
    signature: bytes

@dataclass
class VerificationResponse:
    is_valid: bool

# Although these models are not directly used in the current implementation files,
# they serve as a conceptual structure for request/response payloads and can be
# expanded for more complex data handling or validation if the project grows.
