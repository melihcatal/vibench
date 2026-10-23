from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str
    encryption_context: Optional[dict[str, str]] = None

@dataclass
class DecryptionRequest:
    ciphertext_blob: bytes
    encryption_context: Optional[dict[str, str]] = None

@dataclass
class SignatureRequest:
    message: str
    key_id: str
    signing_algorithm: str

@dataclass
class VerificationRequest:
    message: str
    signature: bytes
    key_id: str
    signing_algorithm: str
