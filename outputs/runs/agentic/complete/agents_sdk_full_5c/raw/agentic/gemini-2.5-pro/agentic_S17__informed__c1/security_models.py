# security_models.py
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class EncryptionPayload:
    key_id: str
    plaintext: bytes

@dataclass
class DecryptionPayload:
    key_id: str
    ciphertext: bytes

@dataclass
class SignPayload:
    key_name: str # Name of the key in the vault
    key_version: Optional[str]
    data_to_sign: bytes

@dataclass
class VerifyPayload:
    key_name: str # Name of the key in the vault
    key_version: Optional[str]
    data_to_verify: bytes
    signature: bytes

@dataclass
class EnvelopeEncryptionResult:
    wrapped_data_key: bytes
    ciphertext: bytes

@dataclass
class AuditLog:
    event_name: str
    user: str
    timestamp: str
    details: dict
