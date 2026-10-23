from typing import TypedDict, Dict, Any, List
from dataclasses import dataclass

@dataclass
class EncryptRequest:
    plaintext: bytes
    key_id: str

@dataclass
class DecryptRequest:
    ciphertext_blob: bytes

@dataclass
class EnvelopeEncryptRequest:
    plaintext: bytes
    key_id: str

@dataclass
class EnvelopeEncryptResponse:
    ciphertext: bytes
    nonce: bytes
    tag: bytes
    encrypted_key: bytes

@dataclass
class SignRequest:
    message: bytes
    key_id: str
    signing_algorithm: str

@dataclass
class KeyUsageEvent:
    timestamp: str
    operation: str
    key_id: str
    status: str
