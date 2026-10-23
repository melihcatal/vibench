import dataclasses
from typing import Optional, Literal

@dataclasses.dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: Optional[str] = None  # Full KMS key path or identifier

@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: bytes
    encrypted_dek: Optional[bytes] = None # For envelope encryption

@dataclasses.dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: Optional[str] = None # Full KMS key path or identifier
    encrypted_dek: Optional[bytes] = None # For envelope encryption

@dataclasses.dataclass
class DecryptionResponse:
    plaintext: bytes

@dataclasses.dataclass
class SignatureRequest:
    message: bytes
    key_id: Optional[str] = None # Full KMS key path or identifier
    key_version_id: Optional[str] = None # Specific key version for signing

@dataclasses.dataclass
class SignatureResponse:
    signature: bytes

@dataclasses.dataclass
class VerificationRequest:
    message: bytes
    signature: bytes
    key_id: Optional[str] = None # Full KMS key path or identifier
    key_version_id: Optional[str] = None # Specific key version for verification

@dataclasses.dataclass
class VerificationResponse:
    is_valid: bool

